"""
Service for fetching and extracting article content from URLs
"""
import httpx
from readability import Document
import logging
from typing import Dict, List, Optional
import re
import certifi

logger = logging.getLogger(__name__)


class ArticleExtractor:
    """Service for extracting readable content from URLs"""
    
    def __init__(self, timeout: int = 20):
        """
        Initialize article extractor
        """
        self.timeout = timeout
        print("Using certifi CA bundle:", certifi.where())
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }
    
    async def fetch_and_extract(self, url: str, client: Optional[httpx.AsyncClient] = None) -> Dict[str, str]:
        """
        Fetch URL and extract readable article content
        """
        # Ensure HTTPS
        if url.startswith("http://"):
            url = url.replace("http://", "https://", 1)
        elif not url.startswith("https://"):
            url = f"https://{url}"

        # 1. Detect Wikipedia and use API
        if "wikipedia.org" in url.lower():
            return await self._fetch_wikipedia_api(url, client)

        # 2. Regular Scraping for other sites
        try:
            logger.info(f"Fetching URL: {url}")
            
            if client:
                response = await client.get(url)
            else:
                async with httpx.AsyncClient(
                    headers=self.headers, 
                    follow_redirects=True, 
                    timeout=self.timeout,
                    verify=certifi.where()
                ) as local_client:
                    response = await local_client.get(url)
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch {url}. Status code: {response.status_code}")
                raise Exception(f"Site returned error status: {response.status_code}")
            
            # Extract readable content
            doc = Document(response.text)
            title = doc.title()
            content = doc.summary()
            
            # Clean HTML tags from content
            clean_content = re.sub('<[^<]+?>', '', content)
            clean_content = re.sub(r'\s+', ' ', clean_content).strip()
            
            logger.info(f"Successfully extracted content from: {url}")
            
            return {
                "url": url,
                "title": title or "Untitled Article",
                "content": clean_content[:5000]
            }
                
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {str(e)}")
            raise Exception(f"Processing error: {str(e)}")

    async def _fetch_wikipedia_api(self, url: str, client: Optional[httpx.AsyncClient] = None) -> Dict[str, str]:
        """Fetch content using Wikipedia REST API instead of scraping"""
        try:
            # Extract page title from URL (e.g., https://en.wikipedia.org/wiki/Artificial_intelligence -> Artificial_intelligence)
            title_match = re.search(r'/wiki/([^/?#]+)', url)
            if not title_match:
                raise ValueError("Could not extract Wikipedia page title from URL")
            
            page_title = title_match.group(1)
            api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{page_title}"
            
            logger.info(f"Using Wikipedia API for: {url}")
            
            if client:
                response = await client.get(api_url)
            else:
                async with httpx.AsyncClient(
                    headers=self.headers, 
                    timeout=self.timeout,
                    verify=certifi.where()
                ) as local_client:
                    response = await local_client.get(api_url)
            
            if response.status_code != 200:
                raise Exception(f"Wikipedia API error: {response.status_code}")
            
            data = response.json()
            title = data.get("title", "Wikipedia Article")
            extract = data.get("extract", "No content found.")
            
            logger.info(f"Successfully fetched Wikipedia data for: {page_title}")
            
            return {
                "url": url,
                "title": title,
                "content": extract[:5000]
            }
        except Exception as e:
            logger.error(f"Wikipedia API fetch failed for {url}: {str(e)}")
            raise Exception(f"Wikipedia API error: {str(e)}")
    
    async def fetch_multiple(self, urls: List[str]) -> List[Dict[str, str]]:
        """
        Fetch and extract content from multiple URLs
        """
        results = []
        
        # Use a persistent client for the entire batch to handle keep-alive properly
        async with httpx.AsyncClient(
            headers=self.headers, 
            follow_redirects=True, 
            timeout=self.timeout,
            verify=certifi.where()
        ) as client:
            for url in urls:
                try:
                    content = await self.fetch_and_extract(url, client=client)
                    results.append(content)
                except Exception as e:
                    logger.warning(f"Skipping {url} due to error: {str(e)}")
                    results.append({
                        "url": url,
                        "title": "Access Error",
                        "content": f"[Could not read source: {str(e)}]"
                    })
        
        return results

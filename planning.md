\# Project Planning



\## Domain

US National Parks — answering visitor questions about wildlife, camping, hiking, and weather.



\## Document Sources

\- Yellowstone: animals, mammals, camping, hiking, visitor centers pages (nps.gov/yell)

\- Grand Canyon: animals, camping, hiking, permits, backcountry permit pages (nps.gov/grca)

\- Yosemite: animals, camping, hiking, reservations, valley hikes pages (nps.gov/yose)

\- Zion: animals, camping, hiking, permits, weather pages (nps.gov/zion)

\- Great Smoky Mountains: animals, camping, hiking, weather, black bears pages (nps.gov/grsm)



\## Retrieval Approach

1\. Scrape NPS pages with BeautifulSoup, save as .txt files

2\. Chunk text into 400-word chunks with 50-word overlap

3\. Embed chunks with all-MiniLM-L6-v2 from sentence-transformers

4\. Store embeddings in ChromaDB with source metadata

5\. At query time: embed question, retrieve top-4 chunks, pass to LLM



\## Chunking Strategy

\- Chunk size: 400 words with 50-word overlap

\- Overlap prevents relevant content from being split across chunk boundaries

\- Word-based splitting fits NPS prose pages well



\## Generation Strategy

\- Model: Groq llama-3.3-70b-versatile (free tier)

\- Grounding: prompt explicitly instructs model to answer only from retrieved context

\- Attribution: source document names appended to every response



\## Evaluation Plan — 5 Test Questions

1\. What wildlife can visitors see at Yellowstone?

2\. How do I get a camping permit at the Grand Canyon?

3\. What are the most popular hikes in Yosemite?

4\. Is Zion National Park open year-round?

5\. What is the best time to visit Great Smoky Mountains?


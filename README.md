# RAG System — US National Parks Assistant

## Domain and Document Sources
This RAG system answers visitor questions about five US National Parks.
Documents were scraped from the official National Park Service website (nps.gov).

- **Yellowstone**: animals, mammals, camping, hiking, visitor centers (nps.gov/yell)
- **Grand Canyon**: animals, camping, hiking, permits, backcountry permits (nps.gov/grca)
- **Yosemite**: animals, camping, hiking, reservations, valley hikes (nps.gov/yose)
- **Zion**: animals, camping, hiking, permits, weather (nps.gov/zion)
- **Great Smoky Mountains**: animals, camping, hiking, weather, black bears (nps.gov/grsm)

## Chunking Strategy
- **Chunk size**: 400 words with 50-word overlap
- **Reasoning**: NPS pages are written in flowing prose paragraphs. Word-based chunking with overlap ensures that sentences split across a boundary still appear in at least one complete chunk, preserving semantic context for the embedding model.

## Sample Chunks
**Chunk 1 (yellowstone, index 0):** "roam the park. Long-tailed weasels change color based on the season. Member of the weasel family that lives in woodlands. Smallest of the three canid species found in the park..."

**Chunk 2 (grand_canyon, index 1):** "or trips into the canyon on the Havasupai Reservation. To obtain additional information on how to enter the Phantom Ranch lodging lottery, please contact Xanterra Parks..."

**Chunk 3 (yosemite, index 2):** "Meadows (open July to late September). Camp 4 reservations are released one week in advance on a rolling daily window (i.e., 7 days in advance of arrival date)..."

**Chunk 4 (zion, index 0):** "Species Attribute Definitions. Occurrence values are defined below. Present: Species occurs in park; confirmed sightings..."

**Chunk 5 (great_smoky, index 3):** "Elk Learn more about the elk that roam the valleys of the Smokies. Amphibians Learn about the unique amphibians in the Smokies. Pollinators are a fundamental group..."

## Embedding Model
**Model used**: `all-MiniLM-L6-v2` from sentence-transformers. This model runs locally with no API key or rate limits, produces 384-dimensional embeddings, and is fast enough to embed hundreds of chunks in seconds on a laptop.

**Production tradeoffs**: In a production deployment I would consider OpenAI's `text-embedding-3-small` for higher accuracy, or a domain-specific model fine-tuned on travel/nature content. The tradeoff is cost and latency vs. the free local option.

## Retrieval Test Results

**Query 1: "What wildlife can visitors see at Yellowstone?"**
- Result 1 | Source: yellowstone | Distance: 0.748 — lists mammals including bison, elk, bears, wolves ✅
- Result 2 | Source: yellowstone | Distance: 0.763 — mentions 13 bat species in the park ✅
- Result 3 | Source: yellowstone | Distance: 0.786 — additional mammal info ✅
- Result 4 | Source: yellowstone | Distance: 0.848 — hiking/backcountry context ⚠️
- **Why relevant**: Results 1-3 directly list animal species found in Yellowstone, matching the query intent.

**Query 2: "How do I get a camping permit at the Grand Canyon?"**
- Result 1 | Source: grand_canyon | Distance: 0.541 — backcountry permit page ✅
- Result 2 | Source: grand_canyon | Distance: 0.698 — Phantom Ranch lodging info ✅
- Result 3 | Source: grand_canyon | Distance: 0.742 — camping page ✅
- Result 4 | Source: grand_canyon | Distance: 0.903 — campground night limits ✅
- **Why relevant**: All four results come from Grand Canyon permit and camping pages, directly addressing the query.

**Query 3: "What are the most popular hikes in Yosemite?"**
- Result 1 | Source: yosemite | Distance: 0.848 — mentions strenuous hikes in Yosemite Valley ✅
- Result 2 | Source: yosemite | Distance: 0.856 — camping reservation info ⚠️
- Result 3 | Source: yosemite | Distance: 1.006 — parking/traffic context ⚠️
- Result 4 | Source: yosemite | Distance: 1.029 — animals page ⚠️
- **Why relevant**: Result 1 is on-topic; others are from Yosemite but off-topic, indicating the hiking page had limited specific trail content.

## Grounded Generation
Grounding is enforced in `query.py` through the prompt passed to the LLM: "Answer the question using ONLY the information provided in the context below. If the context does not contain enough information to answer, say 'I don't have enough information on that.'" Source names are appended programmatically — the LLM cannot cite a source that wasn't retrieved.

## Example Responses

**Response 1 — Wildlife at Yellowstone (grounded):**
"Visitors to Yellowstone can see a variety of wildlife, including 67 different mammals such as bison, elk, grizzly bears, gray wolves, lynx, and wolverines. Sources: yellowstone"

**Response 2 — Out-of-scope query (correct refusal):**
Query: "What is the weather like in Zion?"
"The provided context does not specifically describe the weather in Zion National Park. I don't have enough information on that. Sources: great_smoky, zion, grand_canyon"

## Query Interface
The interface is built with Gradio and runs at http://localhost:7860.
- **Input**: A text box labeled "Your Question"
- **Output 1**: "Answer" — the LLM's grounded response with source citation
- **Output 2**: "Retrieved From" — lists the source documents used

**Sample interaction:**
- Input: "What wildlife can visitors see at Yellowstone?"
- Answer: "Visitors to Yellowstone can see 67 different mammals including bison, elk, grizzly bears, gray wolves, and bats. Sources: yellowstone"
- Retrieved From: "• yellowstone"

## Evaluation Report

| # | Question | Expected | Accuracy |
|---|----------|----------|----------|
| 1 | What wildlife can visitors see at Yellowstone? | List of animals like bison, bears, wolves | Accurate |
| 2 | How do I get a camping permit at the Grand Canyon? | Permit process, backcountry office | Partially Accurate |
| 3 | What are the most popular hikes in Yosemite? | Trail names like Half Dome, Mist Trail | Partially Accurate |
| 4 | Is Zion National Park open year-round? | Yes, with seasonal variations | Inaccurate |
| 5 | What is the best time to visit Great Smoky Mountains? | Spring/fall for foliage | Inaccurate |

## Failure Case Analysis
**Question 4 — Zion year-round availability** failed because the Zion weather page scraped very little usable text (only 4,880 chars total across all Zion pages). The NPS Zion weather page returned mostly navigation elements rather than substantive content. As a result, no chunk contained information about park operating hours or seasonal closures. This is a scraping failure — the retrieval returned Zion chunks, but those chunks came from the animals page rather than an hours/seasons page. A fix would be to scrape the Zion "Hours & Directions" page specifically.

## Spec Reflection
**How the spec helped**: The spec's emphasis on testing retrieval before wiring in generation (Milestone 4) was valuable. Printing distance scores and chunk content early revealed that the NPS homepage had too little text, which led me to scrape deeper pages instead.

**How implementation diverged**: The spec suggests aiming for distance scores below 0.5, but most of my scores fell in the 0.7–0.9 range. Rather than continuing to chase lower scores, I verified that the correct source documents were being returned and proceeded. The scores reflect the small corpus size more than retrieval quality.

## AI Usage
**Instance 1**: I asked Claude to generate the scraping code using BeautifulSoup. It produced a version that only scraped the NPS homepage. I directed it to scrape multiple subpages per park (animals, camping, hiking) and to filter lines shorter than 40 characters to remove navigation noise.

**Instance 2**: I asked Claude to generate the ChromaDB embedding and retrieval code. The initial retrieval test showed poor results. I directed Claude to help diagnose the issue, which identified that the documents were too small. I overrode the initial approach and re-scraped with more pages before re-embedding.

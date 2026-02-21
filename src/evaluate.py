import asyncio

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from ragas import EvaluationDataset, SingleTurnSample
from ragas.evaluation import evaluate
from ragas.llms import llm_factory
from openai import AsyncOpenAI

from backend.documents.web_documents import WebDocuments
from backend.documents.url_ranker import UrlRanker
from backend.llm.llm_factory import LLMFactory
from backend.llm.llm_service import LLMService
from backend.rag.rag_engine import RagEngine

SAMPLES_COUNT = 10


async def evaluate_rag():
    queries = [
        "Who discovered the Galapagos Islands and how?",
        "What is Brooklyn–Battery Tunnel?",
        "Are Penguins found in the Galapagos Islands?",
        "How many languages are spoken in New York?",
        "In which countries are snow leopards found?",
        "What are the threats to penguin populations?",
        "What is the economic significance of New York City?",
        "How did New York City get its name?",
        "How did Galapagos Islands get its name?",
        "What is the significance of the Statue of Liberty in New York City?",
    ]

    ground_truths = [
        "The Galapagos Islands were discovered in 1535 by the bishop of Panama, Tomás de Berlanga, whose ship had drifted off course while en route to Peru. He named them Las Encantadas (“The Enchanted”), and in his writings he marveled at the thousands of large galápagos (tortoises) found there. Numerous Spanish voyagers stopped at the islands from the 16th century, and the Galapagos also came to be used by pirates and by whale and seal hunters. ",
        "The Brooklyn-Battery Tunnel (officially known as the Hugh L. Carey Tunnel) is the longest continuous underwater vehicular tunnel in North America and runs underneath Battery Park, connecting the Financial District in Lower Manhattan to Red Hook in Brooklyn.[586]",
        "Penguins live on the galapagos islands side by side with tropical animals.",
        "As many as 800 languages are spoken in New York.",
        "Siberia, Tajikistan, Kyrgyzstan, Uzbekistan, Kazakhstan, Afghanistan, Pakistan, India, Nepal, Bhutan, Mongolia, and Tibet.",
        "The threats are numerous, including habitat loss, pollution, disease, and reduced food availability due to commercial fishing. Climate change is of particular concern for many species of penguin, as the sea ice that they depend on to find food or build nests is melting before their eyes.",
        "New York City's economic significance is vast, as it serves as the global financial capital, housing Wall Street and major financial institutions. Its diverse economy spans technology, media, healthcare, education, and more, making it resilient to economic fluctuations. NYC is a hub for international business, attracting global companies, and boasts a large, skilled labor force. Its real estate market, tourism, cultural industries, and educational institutions further fuel its economic prowess. The city's transportation network and global influence amplify its impact on the world stage, solidifying its status as a vital economic player and cultural epicenter.",
        "New York City got its name when it came under British control in 1664. King Charles II of England granted the lands to his brother, the Duke of York, who named the city New York in his own honor.",
        "Tomás de Berlanga, who discovered the islands, named them Las Encantadas (“The Enchanted”), and in his writings he marveled at the thousands of large galápagos (tortoises) found there. Numerous Spanish voyagers stopped at the islands from the 16th century, and the Galapagos also came to be used by pirates and by whale and seal hunters.",
        "The Statue of Liberty in New York City holds great significance as a symbol of the United States and its ideals of liberty and peace. It greeted millions of immigrants who arrived in the U.S. by ship in the late 19th and early 20th centuries, representing hope and freedom for those seeking a better life. It has since become an iconic landmark and a global symbol of cultural diversity and freedom.",
    ]

    results = [
        {"url": "https://en.wikipedia.org/wiki/New_York_City"},
        {"url": "https://en.wikipedia.org/wiki/Snow_leopard"},
        {"url": "https://www.britannica.com/place/Galapagos-Islands"},
        {
            "url": "https://www.birdlife.org/birds/penguins/#:~:text=The%20threats%20are%20numerous%2C%20including,is%20melting%20before%20their%20eyes."
        },
    ]

    for result in results:
        print(result["url"])
    url_ranker = UrlRanker()
    webdoc = WebDocuments(results, "", url_ranker)
    await webdoc.generate_documents()
    docs = webdoc.get_documents()

    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    llm = LLMFactory.create_llm("openvino", "rupeshs/jan-nano-int4-ov", "CPU")
    results = []
    contexts = []
    llm_service = LLMService(llm)
    rag_engine = RagEngine(embeddings_model=embeddings, llm_service=llm_service)
    rag_engine.load_documents(docs)
    for query in queries[:SAMPLES_COUNT]:
        rag_stream = rag_engine.get_answer_stream(query, False, False)
        answer = ""
        for chunk in rag_stream:
            answer += chunk
        results.append(answer)
        contexts.append(rag_engine.get_context())

    samples = []

    for i in range(SAMPLES_COUNT):
        samples.append(
            SingleTurnSample(
                user_input=queries[i],
                retrieved_contexts=[contexts[i]],
                response=results[i],
                reference=ground_truths[i],
            )
        )
    evaluation_dataset = EvaluationDataset(samples=samples)
    print(evaluation_dataset.to_pandas())

    client = AsyncOpenAI()
    evaluator_llm = llm_factory("gpt-4o-mini", client=client)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    result = evaluate(
        dataset=evaluation_dataset, llm=evaluator_llm, embeddings=embeddings
    )

    print(result)
    result.to_pandas()


asyncio.run(evaluate_rag())

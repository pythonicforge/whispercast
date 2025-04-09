import os
from groq import Groq
from utils import logger
from dotenv import load_dotenv

load_dotenv()

def extract_llama_core_text(response: str) -> str:
    """
    Extract content between lines containing only '---'.
    If not found, fallback to the full response.
    """
    lines = response.strip().splitlines()
    inside = False
    result = []

    for line in lines:
        if line.strip().startswith("---"):
            inside = not inside
            continue
        if inside:
            result.append(line)

    return "\n".join(result).strip() if result else response.strip()

def clean_placeholders(text, name="Sara", podcast_name="WhisperCast"):
    text = text.replace("[Podcast Name]", podcast_name)
    text = text.replace("[Name]", name)
    return text

@logger.catch
def generate_podcast_script(topic: str, content: str, duration: int = 5) -> str:
    """
    Generate a podcast script using Groq's LLaMA 3 model – base + expanded.
    """
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    base_prompt = f"""
            You are a podcast host giving a solo monologue episode about the topic: "{topic}".

            Write a clean, casual podcast script that lasts around 5-6 minutes (~600-700 words).
            Keep it natural and engaging — like a friendly radio host speaking alone.

            Avoid any scene directions like [pause], or labels like "Host:".
            Just pure, natural dialogue.

            Use the info below to guide your content:
            \"\"\"{content}\"\"\"
            """

    try:
        logger.info("Generating base script...")
        base_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": base_prompt.strip()}],
            model="llama3-70b-8192",
            temperature=0.8,
            max_tokens=4096,
        )

        base_script = base_completion.choices[0].message.content

        expand_prompt = f"""
                You are an expert podcast scriptwriter. Here's a podcast monologue:

                \"\"\"{base_script}\"\"\"

                Expand this script to be around 2000–4000 words. 
                Keep the tone casual, fun, and informative — like a solo podcast host.
                Don’t change the original style — just build on it and add more insights, examples, and natural flow.
            """

        logger.info("Expanding script...")
        expanded_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": expand_prompt.strip()}],
            model="llama3-70b-8192",
            temperature=0.75,
            max_tokens=8192
        )

        pre_final_script = expanded_completion.choices[0].message.content

        final_prompt = f"""
                You are an expert podcast scriptwriter. Here's a podcast monologue:

                \"\"\"{pre_final_script}\"\"\"

                Expand this script to be around 2000–4000 words. 
                Keep the tone casual, fun, and informative — like a solo podcast host.
                Don’t change the original style — just build on it and add more insights, examples, and natural flow.
            """
        
        logger.info("Finalising script...")
        expanded_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": final_prompt.strip()}],
            model="llama3-70b-8192",
            temperature=0.75,
            max_tokens=8192
        )

        final_script = expanded_completion.choices[0].message.content

        return clean_placeholders(extract_llama_core_text(final_script))

    except Exception as e:
        logger.critical(f"Podcast generation failed: {e}")
        return ""

def split_large_content(content: str, max_tokens: int = 6000) -> list:
    """
    Split content into smaller chunks to fit within the token limit.
    """
    words = content.split()
    chunk_size = max_tokens // 2  # Approximate words per chunk
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

@logger.catch
def generate_audiobook(content: str):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    chunks = split_large_content(content)
    logger.info(f"Content split into {len(chunks)} chunks for processing.")

    audiobook_script = []
    for i, chunk in enumerate(chunks):
        base_prompt = f"""
                You're an audiobook narrator with a relaxed, witty, and Gen-Z-friendly tone.

                You're explaining the following content in a natural, engaging, and storytelling way — not like a lecture, but more like you're walking your friend through the topic casually, adding personality, insights, and relatable metaphors where it fits.

                The audiobook should feel like you're speaking directly to the listener — like a human, not a robot.

                Make it flow like a story or an engaging TED-style explanation. Don’t use scene directions, and avoid labeling (like "Narrator:" or "Chapter 1").

                Use the following content as your knowledge base — explain it, break it down, and make it hit:
                \"\"\"{chunk}\"\"\"
                """
        logger.info(f"Processing chunk {i + 1}/{len(chunks)}")
        try:
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": base_prompt}],
                temperature=0.8,
                max_tokens=8192
            )
            audiobook_script.append(completion.choices[0].message.content.strip())
        except Exception as e:
            logger.error(f"Error processing chunk {i + 1}: {e}")
            continue

    final_script = "\n".join(audiobook_script)
    logger.success("Audiobook script generated successfully!")
    return final_script
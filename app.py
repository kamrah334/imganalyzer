import gradio as gr
import pandas as pd
import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from deepai_client import enhance_seo_text
from seo import clean_keywords, clean_title

# Load BLIP model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def analyze_images(images):
    results = []
    for img in images:
        image = Image.open(img).convert("RGB")
        inputs = processor(image, return_tensors="pt")
        caption_ids = model.generate(**inputs)
        caption = processor.decode(caption_ids[0], skip_special_tokens=True)

        seo_text = enhance_seo_text(caption)

        # Try to split title & keywords
        if "Keywords:" in seo_text:
            title_part, keywords_part = seo_text.split("Keywords:", 1)
        else:
            parts = seo_text.split("\n", 1)
            title_part = parts[0]
            keywords_part = parts[1] if len(parts) > 1 else ""

        title = clean_title(title_part.strip())
        keywords = clean_keywords(keywords_part.strip())

        results.append({
            "Filename": os.path.basename(img.name),
            "Title": title,
            "Keywords": keywords
        })

    df = pd.DataFrame(results)
    csv_path = "/mnt/data/results.csv"
    df.to_csv(csv_path, index=False)
    return df, csv_path

with gr.Blocks() as demo:
    gr.Markdown("## 📸 SEO Image Analyzer")
    with gr.Row():
        image_input = gr.File(label="Upload Images", file_types=[".png", ".jpg", ".jpeg"], file_count="multiple")
    analyze_btn = gr.Button("Analyze")
    output_table = gr.Dataframe()
    download_link = gr.File()

    analyze_btn.click(analyze_images, inputs=[image_input], outputs=[output_table, download_link])

if __name__ == "__main__":
    demo.launch()

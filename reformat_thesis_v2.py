import re

def main():
    with open("main.tex.bak", "r") as f:
        content = f.read()

    # 1. Clean up known table references (replacing specific lines containing \textbf{??})
    replacements = {
        # Table references
        r"summarized in Table \\textbf\{\?\?\}\.": r"summarized in Table~\\ref{tab:table1}.",
        r"database, comparing their properties in Table \\textbf\{\?\?\}(~?)\.": r"database, comparing their properties in Table~\\ref{tab:table2}.",
        r"are detailed in Table \\textbf\{\?\?\}\.": r"are detailed in Table~\\ref{tab:table5}.",
        r"Filter\} is implemented as detailed in Table \\textbf\{\?\?\}\.": r"Filter} is implemented as detailed in Table~\\ref{tab:table7}.",
        r"the hardware components are detailed in Table \\textbf\{\?\?\}\.": r"the hardware components are detailed in Table~\\ref{tab:table8}.",
        r"driver pins is mapped in Table \\textbf\{\?\?\}\.": r"driver pins is mapped in Table~\\ref{tab:table9}.",
        r"state as shown in Table \\textbf\{\?\?\}\.": r"state as shown in Table~\\ref{tab:table10}.",
        r"overall training configuration is summarized in Table \\textbf\{\?\?\}\.": r"overall training configuration is summarized in Table~\\ref{tab:table13}.",
        r"identical configurations\. Table \\textbf\{\?\?\} shows the per-class": r"identical configurations. Table~\\ref{tab:table23} shows the per-class",
        r"Table \\textbf\{\?\?\}, showing the continuous reduction": r"Table~\\ref{tab:table24}, showing the continuous reduction",
        r"Table \\textbf\{\?\?\} outlines the validation results for YOLO26n": r"Table~\\ref{tab:table25} outlines the validation results for YOLO26n",
        r"\(KPIs\) is sum-marized in Table \\textbf\{\?\?\}\.": r"(KPIs) is summarized in Table~\\ref{tab:table26}.",
        r"impacts are detailed in Table \\textbf\{\?\?\}\.": r"impacts are detailed in Table~\\ref{tab:table27}.",
        r"rules are summarized in Table \\textbf\{\?\?\}\.": r"rules are summarized in Table~\\ref{tab:table28}.",
        r"detailed in Table \\textbf\{\?\?\} and Table \\textbf\{\?\?\}\.": r"detailed in Table~\\ref{tab:table14} and Table~\\ref{tab:table15}.",
        # Fig references
        r"results are illustrated in Fig\. \\textbf\{\?\?\}\.": r"results are illustrated in Fig.~\\ref{fig:fig27}."
    }

    for pattern, repl in replacements.items():
        content = re.sub(pattern, repl, content)

    content = content.replace("score (85\\%). A comparative summary is presented in Table \\textbf{??}.", "score (85\\%). A comparative summary is presented in Table~\\ref{tab:table6}.")
    content = content.replace("Table \\textbf{??}.\n\\end{quote}\n\nTABLE 19:", "Table~\\ref{tab:table19}.\n\\end{quote}\n\nTABLE 19:")
    content = content.replace("A summary of the APMS software technology stack is documented in Table\n4.", "A summary of the APMS software technology stack is documented in Table~\\ref{tab:table4}.")

    # 2. Replace Tables 13, 14, 16 with standard tables
    t13_old = r"""TABLE 13: Mobile YOLO Training Configuration
\end{quote}

\includegraphics[width=3.62639in,height=\textheight,keepaspectratio]{./media/image49.png}

\begin{quote}
\textbf{Parameter Configuration Value}
\end{quote}

\includegraphics[width=3.62639in,height=\textheight,keepaspectratio]{./media/image49.png}

\begin{quote}
Pre-trained Model Base yolov8n.pt (COCO dataset) Backbone Freezing Layer
freeze=10 (layers 1--10 frozen) Optimizer AdamW (learning rate = 0.001)

Batch Size 16

Training Epochs 120 (with early stopping patience = 30) Input Resolution
640 \emph{$\times$} 640 pixels

Augmented Dataset Size 327 images (297 train, 30 validation)"""

    t13_new = r"""\begin{table}[htbp]
\centering
\caption{Mobile YOLO Training Configuration\label{tab:table13}}
\begin{tabular}{ll}
\toprule
\textbf{Parameter} & \textbf{Configuration Value} \\
\midrule
Pre-trained Model Base & yolov8n.pt (COCO dataset) \\
Backbone Freezing Layer & freeze=10 (layers 1--10 frozen) \\
Optimizer & AdamW (learning rate = 0.001) \\
Batch Size & 16 \\
Training Epochs & 120 (with early stopping patience = 30) \\
Input Resolution & $640 \times 640$ pixels \\
Augmented Dataset Size & 327 images (297 train, 30 validation) \\
\bottomrule
\end{tabular}
\end{table}"""

    content = content.replace(t13_old, t13_new)

    t14_old = r"""TABLE 14: SAHI Inference Configuration Parameters
\end{quote}

\includegraphics[width=2.53264in,height=\textheight,keepaspectratio]{./media/image49.png}

\begin{quote}
\textbf{SAHI Parameter Configuration Value}
\end{quote}

\includegraphics[width=2.53264in,height=\textheight,keepaspectratio]{./media/image49.png}

\begin{quote}
Slice Height 320 pixels

Slice Width 320 pixels Overlap Height Ratio 0.2 Overlap Width Ratio 0.2
Confidence Threshold 0.78

Inference Device CUDA GPU (cuda:0)"""

    t14_new = r"""\begin{table}[htbp]
\centering
\caption{SAHI Inference Configuration Parameters\label{tab:table14}}
\begin{tabular}{ll}
\toprule
\textbf{SAHI Parameter} & \textbf{Configuration Value} \\
\midrule
Slice Height & 320 pixels \\
Slice Width & 320 pixels \\
Overlap Height Ratio & 0.2 \\
Overlap Width Ratio & 0.2 \\
Confidence Threshold & 0.78 \\
Inference Device & CUDA GPU (cuda:0) \\
\bottomrule
\end{tabular}
\end{table}"""

    content = content.replace(t14_old, t14_new)

    t16_old = r"""TABLE 16: Visual Servoing Control Loop Parameters

\includegraphics[width=3.675in,height=\textheight,keepaspectratio]{./media/image49.png}

\begin{quote}
\textbf{Parameter Operational Value}
\end{quote}

\includegraphics[width=3.675in,height=\textheight,keepaspectratio]{./media/image49.png}

\begin{quote}
Frame Center (\emph{Xcenter} ) 320 pixels Alignment Zone
(\emph{$\theta$\textsubscript{align}}) \emph{$\pm$}80 pixels

Stop Threshold (Medicine) 200 pixels (average bounding box size) Stop
Threshold (Box) 180 pixels (average bounding box size) Arm Gantry Grab
Delay 10 seconds

Pulsed Backward Duration 1.5 seconds (0.12s pulse on, 0.1s off) Search
Sweep Timeout 2.0 seconds per rotation step"""

    t16_new = r"""\begin{table}[htbp]
\centering
\caption{Visual Servoing Control Loop Parameters\label{tab:table16}}
\begin{tabular}{ll}
\toprule
\textbf{Parameter} & \textbf{Operational Value} \\
\midrule
Frame Center ($X_{center}$) & 320 pixels \\
Alignment Zone ($\theta_{align}$) & $\pm 80$ pixels \\
Stop Threshold (Medicine) & 200 pixels (average bounding box size) \\
Stop Threshold (Box) & 180 pixels (average bounding box size) \\
Arm Gantry Grab Delay & 10 seconds \\
Pulsed Backward Duration & 1.5 seconds (0.12s pulse on, 0.1s off) \\
Search Sweep Timeout & 2.0 seconds per rotation step \\
\bottomrule
\end{tabular}
\end{table}"""

    content = content.replace(t16_old, t16_new)

    # 3. Clean up standard longtables and insert captions
    for table_num in range(1, 30):
        if table_num in [13, 14, 16]:
            continue
        
        pattern_str = rf"TABLE\s+{table_num}:\s*([^\n\r]+(?:\n[^\n\r]+)?)"
        match = re.search(pattern_str, content)
        if not match:
            continue
        
        caption_text = match.group(1).strip()
        caption_text = re.sub(r"\\end\{quote\}", "", caption_text).strip()
        
        start_pos = match.end()
        lt_match = re.search(r"\\begin\{longtable\}\[]\{(@\{\}\s*(?:>\{\\raggedright\\arraybackslash\}p\{.*?\}\s*)*@\{\})\}", content[start_pos:])
        if not lt_match:
            continue
        
        lt_start = start_pos + lt_match.start()
        lt_end = start_pos + lt_match.end()
        cols_spec = lt_match.group(1)
        
        line_start = content.rfind("\n", 0, match.start()) + 1
        line_prefix = content[line_start:match.start()].strip()
        
        additional_header = ""
        if table_num == 20:
            additional_header = r"""\toprule
\textbf{Segment} & \textbf{Model} & \textbf{n} & \textbf{R\textsuperscript{2} (\%)} & \textbf{RMSE (Units)} & \textbf{MAE (Units)} \\
\midrule"""
        elif table_num == 24:
            additional_header = r"""\toprule
\textbf{Epoch} & \textbf{Bounding Box Loss} & \textbf{Classification Loss} & \textbf{mAP@50} & \textbf{mAP@50-95} \\
\midrule"""
        
        new_lt_start = f"\\begin{{longtable}}[]{{{cols_spec}}}\n\\caption{{{caption_text}\\label{{tab:table{table_num}}}}}\\\\\n"
        if additional_header:
            new_lt_start += additional_header
            
        prefix = ""
        if "gap remains" in line_prefix:
            prefix = "gap remains, as summarized in Table~\\ref{tab:table3}.\n\n"
        elif line_prefix and not line_prefix.startswith(r"\begin{quote}"):
            prefix = line_prefix + "\n\n"
            
        content = content[:match.start() - len(line_prefix)] + prefix + new_lt_start + content[lt_end:]

    content = re.sub(r"\{\s*\\def\s*\\LTcaptype\s*\{\s*none\s*\}[\s\S]*?\\begin\{longtable\}", r"\\begin{longtable}", content)
    content = re.sub(r"\\end\{longtable\}\s*\}", r"\\end{longtable}", content)

    # Delete Table 20/24 header images/quotes
    content = re.sub(r"\\includegraphics\[width=4\.80278in,height=\\textheight,keepaspectratio\]\{.*?image49\.png\}\s*\\begin\{quote\}\s*\\textbf\{Segment Model[\s\S]*?\\end\{quote\}", "", content)
    content = re.sub(r"\\includegraphics\[width=4\.56667in,height=\\textheight,keepaspectratio\]\{.*?image49\.png\}\s*\\begin\{quote\}\s*\\textbf\{Epoch Bounding[\s\S]*?\\end\{quote\}", "", content)

    print("Tables reformatted.")

    # Remove quote environments before block parsing
    content = re.sub(r"\\begin\{quote\}", "", content)
    content = re.sub(r"\\end\{quote\}", "", content)

    # 4. Block-by-block parsing of the content
    # Split the document by double newlines
    blocks = content.split("\n\n")
    output_blocks = []
    
    accumulated_images = []
    accumulated_subcaps = []
    
    for i, block in enumerate(blocks):
        block_clean = block.strip()
        if not block_clean:
            continue
            
        # Check if block is a figure caption:
        # e.g., Fig. 1: ... or Figure: ...
        fig_match = re.match(r"^(Fig\.\s+(\d+)|Figure\s+(\d+)|Figure)\s*:\s*([\s\S]*)", block_clean)
        
        if fig_match:
            fig_num = fig_match.group(2) if fig_match.group(2) else fig_match.group(3)
            caption_text = fig_match.group(4).strip()
            
            # Format label
            if fig_num:
                label = f"fig:fig{fig_num}"
            else:
                clean_title = re.sub(r"[^\w\s]", "", caption_text.lower())
                label = "fig:" + "_".join(clean_title.split()[:3])
                
            # If we have accumulated sub-captions, append them to the caption text
            sub_cap_str = ""
            if accumulated_subcaps:
                sub_cap_str = ": " + " ".join(accumulated_subcaps)
                # Clean up newlines and spaces
                sub_cap_str = re.sub(r"\s+", " ", sub_cap_str)
                
            full_caption = caption_text + sub_cap_str
            full_caption = re.sub(r"\s+", " ", full_caption)
            
            # Assemble figure environment
            if accumulated_images:
                img_block = "\n".join(accumulated_images)
            else:
                # Fallback if no images found (should not happen)
                img_block = "% Warning: No image found"
                
            figure_block = f"""\\begin{{figure}}[htbp]
\\centering
{img_block}
\\caption{{{full_caption}\\label{{{label}}}}}
\\end{{figure}}"""
            
            output_blocks.append(figure_block)
            
            # Clear accumulators
            accumulated_images = []
            accumulated_subcaps = []
            
        # Check if block is an image block (starts with \includegraphics)
        elif block_clean.startswith("\\includegraphics") or block_clean.startswith("\\pandocbounded{\\includegraphics"):
            # Extract all \includegraphics commands
            imgs = re.findall(r"\\includegraphics\[.*?\]\{.*?\}", block_clean)
            accumulated_images.extend(imgs)
            
            # Remove \includegraphics commands from the block to see if there is sub-caption text left
            remaining_text = re.sub(r"\\includegraphics\[.*?\]\{.*?\}", "", block_clean).strip()
            if remaining_text:
                accumulated_subcaps.append(remaining_text)
                
            # Do NOT output this block yet (it will be wrapped in the figure environment)
            
        else:
            # If we see any other text, but we have accumulated images/subcaps:
            # Wait! Sometimes we might have a text paragraph between images and a figure caption?
            # No, in this thesis, images and their captions are always in consecutive blocks.
            # So if we see standard text, we just output it.
            output_blocks.append(block)

    # Reassemble content
    content = "\n\n".join(output_blocks)

    # Clean up double empty lines
    content = re.sub(r"\n\s*\n\s*\n", "\n\n", content)

    with open("main.tex", "w") as f:
        f.write(content)

    print("Figures and quotes reformatted successfully!")

if __name__ == "__main__":
    main()

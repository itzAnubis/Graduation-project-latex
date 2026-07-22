import re
import shutil

# Make a backup of main.tex first
shutil.copyfile("main.tex", "main.tex.bak")

with open("main.tex", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Preamble replacement
# Find the start of \begin{document}
doc_start_idx = content.find(r"\begin{document}")
if doc_start_idx == -1:
    raise ValueError("Could not find \\begin{document} in main.tex")

# Everything before \begin{document} is the preamble
preamble = content[:doc_start_idx]

# Define the new preamble
new_preamble = r"""% Options for packages loaded elsewhere
\PassOptionsToPackage{unicode}{hyperref}
\PassOptionsToPackage{hyphens}{url}
\documentclass[12pt,a4paper,oneside]{report}
\usepackage{xcolor}
\usepackage{amsmath,amssymb}
\setcounter{secnumdepth}{3} % enable section numbering
\usepackage{iftex}
\ifPDFTeX
  \usepackage[T1]{fontenc}
  \usepackage[utf8]{inputenc}
  \usepackage{textcomp} % provide euro and other symbols
\else % if luatex or xetex
  \usepackage{unicode-math} % this also loads fontspec
  \defaultfontfeatures{Scale=MatchLowercase}
  \defaultfontfeatures[\rmfamily]{Ligatures=TeX,Scale=1}
\fi
\usepackage{times}
\usepackage{titlesec}
\usepackage[normalem]{ulem}
\usepackage{setspace}
\singlespacing

% Margins
\usepackage[margin=1in]{geometry}

% Chapter (Main Heading): Bold, 16pt, Center-aligned, ALL CAPS
\titleformat{\chapter}[block]
  {\normalfont\fontsize{16}{20}\bfseries\filcenter\MakeUppercase}
  {\chaptertitlename\ \thechapter:\ }
  {0pt}
  {}
\titlespacing*{\chapter}{0pt}{-20pt}{20pt}

% Section (Sub-heading): Bold, 14pt, Left-aligned
\titleformat{\section}[block]
  {\normalfont\fontsize{14}{18}\bfseries}
  {\thesection\ }
  {0pt}
  {}

% Subsection (Side heading): Bold, 14pt, Left-aligned, Underlined
\titleformat{\subsection}[block]
  {\normalfont\fontsize{14}{18}\bfseries}
  {}
  {0pt}
  {\uline}

\usepackage{lmodern}
\ifPDFTeX\else
  % xetex/luatex font selection
\fi
% Use upquote if available, for straight quotes in verbatim environments
\IfFileExists{upquote.sty}{\usepackage{upquote}}{}
\IfFileExists{microtype.sty}{% use microtype if available
  \usepackage[]{microtype}
  \UseMicrotypeSet[protrusion]{basicmath} % disable protrusion for tt fonts
}{}
\makeatletter
\@ifundefined{KOMAClassName}{% if non-KOMA class
  \IfFileExists{parskip.sty}{%
    \usepackage{parskip}
  }{% else
    \setlength{\parindent}{0pt}
    \setlength{\parskip}{6pt plus 2pt minus 1pt}}
}{% if KOMA class
  \KOMAoptions{parskip=half}}
\makeatother
\usepackage{longtable,booktabs,array}
\newcounter{none} % for unnumbered tables
\usepackage{calc} % for calculating minipage widths
% Correct order of tables after \paragraph or \subparagraph
\usepackage{etoolbox}
\makeatletter
\patchcmd\longtable{\par}{\if@noskipsec\mbox{}\fi\par}{}{}
\makeatother
% Allow footnotes in longtable head/foot
\IfFileExists{footnotehyper.sty}{\usepackage{footnotehyper}}{\usepackage{footnote}}
\makesavenoteenv{longtable}
\usepackage{graphicx}
\makeatletter
\newsavebox\pandoc@box
\newcommand*\pandocbounded[1]{% scales image to fit in text height/width
  \sbox\pandoc@box{#1}%
  \Gscale@div\@tempa{\textheight}{\dimexpr\ht\pandoc@box+\dp\pandoc@box\relax}%
  \Gscale@div\@tempb{\linewidth}{\wd\pandoc@box}%
  \ifdim\@tempb\p@<\@tempa\p@\let\@tempa\@tempb\fi% select the smaller of both
  \ifdim\@tempa\p@<\p@\scalebox{\@tempa}{\usebox\pandoc@box}%
  \else\usebox{\pandoc@box}%
  \fi%
}
% Set default figure placement to htbp
\def\fps@figure{htbp}
\makeatother
\ifLuaTeX
  \usepackage{luacolor}
  \usepackage[soul]{lua-ul}
\else
  \usepackage{soul}
\fi
\setlength{\emergencystretch}{3em} % prevent overfull lines
\providecommand{\tightlist}{%
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\usepackage{bookmark}
\IfFileExists{xurl.sty}{\usepackage{xurl}}{} % add URL line breaks if available
\urlstyle{same}
\hypersetup{
  hidelinks,
  pdfcreator={LaTeX via pandoc}}

\author{}
\date{}
"""

body = content[doc_start_idx:]

# 2. Extract abstract text and replace title page/front matter
# Abstract text starts after \textbf{Abstract} and ends before \textbf{CONTENTS}
abstract_marker = r"\textbf{Abstract}"
contents_marker = r"\textbf{CONTENTS}"

abs_start = body.find(abstract_marker)
contents_start = body.find(contents_marker)

if abs_start != -1 and contents_start != -1:
    abstract_text = body[abs_start + len(abstract_marker):contents_start].strip()
    # clean up quote and enumerate environments inside the abstract text
    abstract_text = re.sub(r'\\begin{quote}\s*', '', abstract_text)
    abstract_text = re.sub(r'\s*\\end{quote}', '', abstract_text)
    
    # We replace from \begin{document} up to the \end{quote} of the list of tables
    # Find the end of the quote containing lists (which ends with \end{quote} after contents_start)
    quote_end = body.find(r"\end{quote}", contents_start)
    if quote_end != -1:
        front_matter_end = quote_end + len(r"\end{quote}")
    else:
        front_matter_end = contents_start
        
    new_front_matter = r"""\begin{document}

\begin{titlepage}
\centering
\vspace*{1cm}
{\fontsize{16}{20}\bfseries\MakeUppercase{Pharos University in Alexandria}\par}
\vspace{0.3cm}
{\fontsize{14}{18}\bfseries\MakeUppercase{Faculty of Engineering\\Computer Engineering Department}\par}
\vspace{1.5cm}
\includegraphics[width=1.8875in,height=1.37in]{./media/image25.jpg}\par
\vspace{1.5cm}
{\fontsize{16}{20}\bfseries\MakeUppercase{APMS: An Integrated Automated Pharmacy Management System with Intellectual Prescription OCR, Robotic Dispensing, and AI-Driven Inventory Analytics}\par}
\vspace{1.5cm}
{\fontsize{14}{18}\bfseries B.Sc. Graduation Thesis\par}
\vspace{1.5cm}
\begin{minipage}{0.45\textwidth}
\begin{flushleft} \large
\emph{Submitted by:}\\
Ahmed Sherif HAMDY\\
Youssef AHMED\\
Mohamed BAKR\\
Nadia HOSNY\\
Ghada SEDIK\\
Demiana SAID
\end{flushleft}
\end{minipage}
\hfill
\begin{minipage}{0.45\textwidth}
\begin{flushright} \large
\emph{Supervised by:}\\
Dr. Sahar Ghanem
\end{flushright}
\end{minipage}
\vfill
{\large June 2026\par}
\end{titlepage}

\chapter*{ABSTRACT}
\addcontentsline{toc}{chapter}{Abstract}
""" + abstract_text + r"""

\clearpage
\tableofcontents
\clearpage
\listoffigures
\clearpage
\listoftables
\clearpage
"""
    body = new_front_matter + body[front_matter_end:]

# 3. Replace Chapter 1 header
body = re.sub(
    r'\\begin{enumerate}\s*\\def\\labelenumi{\\arabic{enumi}\.}\s*\\item\s*\\textbf{INTRODUCTION}\s*\\end{enumerate}',
    r'\\chapter{INTRODUCTION}\\label{introduction}',
    body
)

# 4. Replace other chapters
body = body.replace(r"\section{LITERATURE REVIEW}\label{literature-review}", r"\chapter{LITERATURE REVIEW}\label{literature-review}")
body = body.replace(r"\section{SYSTEM DESIGN AND METHODOLOGY}\label{system-design-and-methodology}", r"\chapter{SYSTEM DESIGN AND METHODOLOGY}\label{system-design-and-methodology}")
body = body.replace(r"\section{IMPLEMENTATION \& RESULTS}\label{implementation-results}", r"\chapter{IMPLEMENTATION \& RESULTS}\label{implementation-results}")
body = body.replace(r"\section{CONCLUSIONS, ADOPTED ETHICS, AND FUTURE WORK}\label{conclusions-adopted-ethics-and-future-work}", r"\chapter{CONCLUSIONS, ADOPTED ETHICS, AND FUTURE WORK}\label{conclusions-adopted-ethics-and-future-work}")
body = body.replace(r"\section{REFERENCES}\label{references}", "\\chapter*{REFERENCES}\\label{references}\n\\addcontentsline{toc}{chapter}{References}")
body = body.replace(r"\section{Appendix}\label{appendix}", "\\appendix\n\\chapter{APPENDIX}\\label{appendix}")

# 5. Shift headings:
# \subsection -> \section
# \subsubsection -> \subsection
body = body.replace(r"\subsection{", r"\section{")
body = body.replace(r"\subsubsection{", r"\subsection{")

# 6. Replace \ul{ with \uline{ to avoid soul package issues with complex nesting
body = body.replace(r"\ul{", r"\uline{")

# 7. Replace non-ASCII math symbols with standard LaTeX math code
replacements = {
    '≥': r'$\ge$',
    '≤': r'$\le$',
    '±': r'$\pm$',
    '·': r'$\cdot$',
    '×': r'$\times$',
    'Σ': r'$\Sigma$',
    'α': r'$\alpha$',
    'γ': r'$\gamma$',
    'η': r'$\eta$',
    'θ': r'$\theta$',
    'τ': r'$\tau$',
    '→': r'$\rightarrow$',
    '∈': r'$\in$',
    '−': '-',
    '◦': r'$^\circ$',
    'Bodirozˇa': r'Bodiro\v{z}a'
}

for unicode_char, latex_code in replacements.items():
    body = body.replace(unicode_char, latex_code)

# 8. Clean up \textsuperscript{$^\circ$} if any was created from \textsuperscript{◦}
body = body.replace(r"\textsuperscript{$^\circ$}", r"$^\circ$")

# Let's write the complete modified file
with open("main.tex", "w", encoding="utf-8") as f:
    f.write(new_preamble + body)

print("Conversion complete.")

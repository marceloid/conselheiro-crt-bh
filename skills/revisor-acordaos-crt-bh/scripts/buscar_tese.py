#!/usr/bin/env python3
"""
Buscador Rápido de Teses-Paradigma e Ementas do CRT-BH.
Pesquisa nos catálogos em references/teses/ e na base histórica.

Uso:
    python buscar_tese.py "integralização de capital"
    python buscar_tese.py "unidade autônoma"
    python buscar_tese.py "pedologia"
"""

import sys
import os
import re

TESES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../references/teses"))

def search_in_markdown(query: str):
    results = []
    if not os.path.exists(TESES_DIR):
        return results
        
    q_words = [w.lower() for w in query.split() if len(w) > 2]
    if not q_words:
        return results
        
    for fname in os.listdir(TESES_DIR):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(TESES_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
            
        sections = content.split("## ")
        for sec in sections[1:]:
            sec_lower = sec.lower()
            match_score = sum(1 for w in q_words if w in sec_lower)
            if match_score > 0:
                title = sec.split("\n")[0].strip()
                results.append((match_score, fname, title, "## " + sec))
                
    results.sort(key=lambda x: x[0], reverse=True)
    return results

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
        
    query = " ".join(sys.argv[1:]).strip()
    print(f"\n🔍 Buscando teses-paradigma do CRT para: '{query}'...")
    print("=" * 70)
    
    matches = search_in_markdown(query)
    if not matches:
        print(f"Nenhuma tese-paradigma encontrada para o termo '{query}'.")
        print("Tente termos como: 'integralização', 'unidade autônoma', 'pedologia', 'reenquadramento', 'des'.")
        sys.exit(0)
        
    print(f"Foram encontradas {len(matches)} teses-paradigma correspondentes:\n")
    for idx, (score, fname, title, sec_content) in enumerate(matches, 1):
        print(f"[{idx}] 📌 {title} (Fonte: {fname})")
        print("-" * 70)
        lines = sec_content.strip().split("\n")
        # Print up to 25 lines
        for l in lines[1:30]:
            print(f"  {l}")
        if len(lines) > 30:
            print("  ... [mais precedentes no arquivo]")
        print("\n" + "=" * 70 + "\n")

if __name__ == "__main__":
    main()

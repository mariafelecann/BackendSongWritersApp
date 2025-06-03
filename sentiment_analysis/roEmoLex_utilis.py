import re
import pandas as pd
def analizeaza_sentiment_melodie(text, lexicon_cuvinte, lexicon_expresii):

    text = text.lower()
    scor_total = 0
    cuvinte_pozitive = []
    cuvinte_negative = []
    print(lexicon_expresii.items)
    for expresie, scor in lexicon_expresii.items():
        if expresie.lower() in text:
            print(expresie)
            numar_aparitii = len(re.findall(r'\b' + re.escape(expresie) + r'\b', text))
            print(numar_aparitii)
            if numar_aparitii == 0:
                continue
            scor_total += scor * numar_aparitii
            print(scor_total)
            if scor > 0:
                cuvinte_pozitive.extend([expresie] * numar_aparitii)
            else:
                cuvinte_negative.extend([expresie] * numar_aparitii)

            text = text.replace(expresie, '')

    tokens = text.split()
    cuvinte_gasite_in_lexicon = 0

    for token in tokens:
        scor = lexicon_cuvinte.get(token)
        if scor is not None:
            scor_total += scor
            cuvinte_gasite_in_lexicon += 1
            if scor > 0:
                cuvinte_pozitive.append(token)
            else:
                cuvinte_negative.append(token)

    numar_total_cuvinte_semnificative = len(cuvinte_pozitive) + len(cuvinte_negative)

    # Scorul final va fi între -1 (complet negativ) și 1 (complet pozitiv)
    if numar_total_cuvinte_semnificative == 0:
        scor_normalizat = 0
    else:
        scor_normalizat = scor_total / numar_total_cuvinte_semnificative

    return {
        'scor_polaritate': scor_normalizat,
        'scor_brut': scor_total,
        'cuvinte_pozitive': cuvinte_pozitive,
        'cuvinte_negative': cuvinte_negative,
        'nr_cuvinte_semnificative': numar_total_cuvinte_semnificative
    }


def load_roemolex_dual(cale_fisier1, cale_fisier2):
    def load_single_file(cale_fisier):
        try:
            df = pd.read_csv(cale_fisier, sep=';', encoding='utf-8')
            if 'word' not in df.columns or 'Pozitivitate' not in df.columns or 'Negativitate' not in df.columns:
                print(f"Fișierul {cale_fisier} nu conține coloanele necesare.")
                return None

            df = df[['word', 'Pozitivitate', 'Negativitate']]

        except Exception as e:
            print(f"Eroare la citirea fișierului {cale_fisier}: {e}")
            return None

        lex_cuv = {}
        lex_expr = {}

        for index, row in df.iterrows():
            cuvant = str(row['word']).lower()
            scor = 0
            try:
                val_pozitiv = pd.to_numeric(row['Pozitivitate'], errors='coerce')
                val_negativ = pd.to_numeric(row['Negativitate'], errors='coerce')

                if pd.isna(val_pozitiv) or pd.isna(val_negativ):
                    print(f"Atenție: Valoare non-numerică în rândul {index} din {cale_fisier}. Se săre peste rând.")
                    continue

                if val_pozitiv == 1:
                    scor = 1
                elif val_negativ == 1:
                    scor = -1

            except ValueError:
                print(f"Eroare neașteptată la conversia valorilor numerice în rândul {index} din {cale_fisier}. Se săre peste rând.")
                continue

            if scor == 0:

                continue

            if ' ' in cuvant:
                lex_expr[cuvant] = scor
            else:
                lex_cuv[cuvant] = scor

        return lex_cuv, lex_expr

    lex_cuv1, lex_expr1 = load_single_file(cale_fisier1)
    lex_cuv2, lex_expr2 = load_single_file(cale_fisier2)

    if lex_cuv1 is None or lex_cuv2 is None:
        print("Eroare la încărcarea unuia din fișiere.")
        return None, None

    lexicon_cuvinte = {**lex_cuv1, **lex_cuv2}
    lexicon_expresii = {**lex_expr1, **lex_expr2}

    lexicon_expresii = dict(sorted(lexicon_expresii.items(), key=lambda item: len(item[0]), reverse=True))

    return lexicon_cuvinte, lexicon_expresii
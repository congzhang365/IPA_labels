class IPALookup:
    def __init__(self):
        # Master dictionary
        self.data = {
            # --- CONSONANTS ---
            'p': {'type': 'consonant', 'labels': ['voiceless', 'bilabial', 'plosive']},
            'b': {'type': 'consonant', 'labels': ['voiced', 'bilabial', 'plosive']},
            'ɓ': {'type': 'consonant', 'labels': ['voiced', 'bilabial', 'implosive']},
            'ɸ': {'type': 'consonant', 'labels': ['voiceless', 'bilabial', 'fricative']},
            'β': {'type': 'consonant', 'labels': ['voiced', 'bilabial', 'fricative']},
            'f': {'type': 'consonant', 'labels': ['voiceless', 'labiodental', 'fricative']},
            'v': {'type': 'consonant', 'labels': ['voiced', 'labiodental', 'fricative']},
            'ⱱ': {'type': 'consonant', 'labels': ['voiced', 'labiodental', 'flap']},
            't': {'type': 'consonant', 'labels': ['voiceless', 'alveolar', 'plosive']},
            'd': {'type': 'consonant', 'labels': ['voiced', 'alveolar', 'plosive']},
            'ɗ': {'type': 'consonant', 'labels': ['voiced', 'alveolar', 'implosive']},
            'ʈ': {'type': 'consonant', 'labels': ['voiceless', 'retroflex', 'plosive']},
            'ɖ': {'type': 'consonant', 'labels': ['voiced', 'retroflex', 'plosive']},
            'θ': {'type': 'consonant', 'labels': ['voiceless', 'dental', 'fricative']},
            'ð': {'type': 'consonant', 'labels': ['voiced', 'dental', 'fricative']},
            'k': {'type': 'consonant', 'labels': ['voiceless', 'velar', 'plosive']},
            'ɡ': {'type': 'consonant', 'labels': ['voiced', 'velar', 'plosive']},
            'ɠ': {'type': 'consonant', 'labels': ['voiced', 'velar', 'implosive']},
            'q': {'type': 'consonant', 'labels': ['voiceless', 'uvular', 'plosive']},
            'ɢ': {'type': 'consonant', 'labels': ['voiced', 'uvular', 'plosive']},
            'ʛ': {'type': 'consonant', 'labels': ['voiced', 'uvular', 'implosive']},
            'x': {'type': 'consonant', 'labels': ['voiceless', 'velar', 'fricative']},
            'ɣ': {'type': 'consonant', 'labels': ['voiced', 'velar', 'fricative']},
            'χ': {'type': 'consonant', 'labels': ['voiceless', 'uvular', 'fricative']},
            'ʁ': {'type': 'consonant', 'labels': ['voiced', 'uvular', 'fricative']},
            'm': {'type': 'consonant', 'labels': ['voiced', 'bilabial', 'nasal']},
            'ɱ': {'type': 'consonant', 'labels': ['voiced', 'labiodental', 'nasal']},
            'n': {'type': 'consonant', 'labels': ['voiced', 'alveolar', 'nasal']},
            'ɳ': {'type': 'consonant', 'labels': ['voiced', 'retroflex', 'nasal']},
            'ɲ': {'type': 'consonant', 'labels': ['voiced', 'palatal', 'nasal']},
            'ŋ': {'type': 'consonant', 'labels': ['voiced', 'velar', 'nasal']},
            'ɴ': {'type': 'consonant', 'labels': ['voiced', 'uvular', 'nasal']},
            's': {'type': 'consonant', 'labels': ['voiceless', 'alveolar', 'fricative']},
            'z': {'type': 'consonant', 'labels': ['voiced', 'alveolar', 'fricative']},
            'ʃ': {'type': 'consonant', 'labels': ['voiceless', 'postalveolar', 'fricative']},
            'ʒ': {'type': 'consonant', 'labels': ['voiced', 'postalveolar', 'fricative']},
            'ʂ': {'type': 'consonant', 'labels': ['voiceless', 'retroflex', 'fricative']},
            'ʐ': {'type': 'consonant', 'labels': ['voiced', 'retroflex', 'fricative']},
            'ɕ': {'type': 'consonant', 'labels': ['voiceless', 'alveolo-palatal', 'fricative']},
            'ʑ': {'type': 'consonant', 'labels': ['voiced', 'alveolo-palatal', 'fricative']},
            'ç': {'type': 'consonant', 'labels': ['voiceless', 'palatal', 'fricative']},
            'ʝ': {'type': 'consonant', 'labels': ['voiced', 'palatal', 'fricative']},
            'r': {'type': 'consonant', 'labels': ['voiced', 'alveolar', 'trill']},
            'ɾ': {'type': 'consonant', 'labels': ['voiced', 'alveolar', 'tap']},
            'ɽ': {'type': 'consonant', 'labels': ['voiced', 'retroflex', 'flap']},
            'ʀ': {'type': 'consonant', 'labels': ['voiced', 'uvular', 'trill']},
            'ʙ': {'type': 'consonant', 'labels': ['voiced', 'bilabial', 'trill']},
            'ɺ': {'type': 'consonant', 'labels': ['voiced', 'alveolar', 'lateral', 'flap']},
            'l': {'type': 'consonant', 'labels': ['voiced', 'alveolar', 'lateral', 'approximant']},
            'ɬ': {'type': 'consonant', 'labels': ['voiceless', 'alveolar', 'lateral', 'fricative']},
            'ɮ': {'type': 'consonant', 'labels': ['voiced', 'alveolar', 'lateral', 'fricative']},
            'ɭ': {'type': 'consonant', 'labels': ['voiced', 'retroflex', 'lateral', 'approximant']},
            'ʎ': {'type': 'consonant', 'labels': ['voiced', 'palatal', 'lateral', 'approximant']},
            'ʟ': {'type': 'consonant', 'labels': ['voiced', 'velar', 'lateral', 'approximant']},
            'h': {'type': 'consonant', 'labels': ['voiceless', 'glottal', 'fricative']},
            'ɦ': {'type': 'consonant', 'labels': ['voiced', 'glottal', 'fricative']},
            'ħ': {'type': 'consonant', 'labels': ['voiceless', 'pharyngeal', 'fricative']},
            'ʕ': {'type': 'consonant', 'labels': ['voiced', 'pharyngeal', 'fricative']},
            'ʜ': {'type': 'consonant', 'labels': ['voiceless', 'epiglottal', 'fricative']},
            'ʔ': {'type': 'consonant', 'labels': ['voiceless', 'glottal', 'plosive']},
            'ʡ': {'type': 'consonant', 'labels': ['voiceless', 'epiglottal', 'plosive']},
            'ʢ': {'type': 'consonant', 'labels': ['voiced', 'epiglottal', 'fricative']},
            'ɧ': {'type': 'consonant', 'labels': ['voiceless', 'simultaneous', 'postalveolar', 'velar', 'fricative']},
            'w': {'type': 'consonant', 'labels': ['voiced', 'labial-velar', 'approximant']},
            'ʍ': {'type': 'consonant', 'labels': ['voiceless', 'labial-velar', 'fricative']},
            'ɥ': {'type': 'consonant', 'labels': ['voiced', 'labial-palatal', 'approximant']},
            'j': {'type': 'consonant', 'labels': ['voiced', 'palatal', 'approximant']},
            'ɰ': {'type': 'consonant', 'labels': ['voiced', 'velar', 'approximant']},
            'ɹ': {'type': 'consonant', 'labels': ['voiced', 'alveolar', 'approximant']},
            'ɻ': {'type': 'consonant', 'labels': ['voiced', 'retroflex', 'approximant']},
            'ʋ': {'type': 'consonant', 'labels': ['voiced', 'labiodental', 'approximant']},
            'c': {'type': 'consonant', 'labels': ['voiceless', 'palatal', 'plosive']},
            'ɟ': {'type': 'consonant', 'labels': ['voiced', 'palatal', 'plosive']},
            'ʄ': {'type': 'consonant', 'labels': ['voiced', 'palatal', 'implosive']},
            'ʘ': {'type': 'consonant', 'labels': ['bilabial', 'click']},
            'ǀ': {'type': 'consonant', 'labels': ['dental', 'click']},
            'ǃ': {'type': 'consonant', 'labels': ['postalveolar', 'click']},
            'ǂ': {'type': 'consonant', 'labels': ['palatoalveolar', 'click']},
            'ǁ': {'type': 'consonant', 'labels': ['alveolar', 'lateral', 'click']},

            # --- VOWELS ---
            'i': {'type': 'vowel', 'labels': ['close', 'front', 'unrounded']},
            'y': {'type': 'vowel', 'labels': ['close', 'front', 'rounded']},
            'ɪ': {'type': 'vowel', 'labels': ['near-close', 'near-front', 'unrounded']},
            'ʏ': {'type': 'vowel', 'labels': ['near-close', 'near-front', 'rounded']},
            'ɨ': {'type': 'vowel', 'labels': ['close', 'central', 'unrounded']},
            'ʉ': {'type': 'vowel', 'labels': ['close', 'central', 'rounded']},
            'e': {'type': 'vowel', 'labels': ['close-mid', 'front', 'unrounded']},
            'ə': {'type': 'vowel', 'labels': ['mid', 'central', 'unrounded', 'schwa']},
            'ɘ': {'type': 'vowel', 'labels': ['close-mid', 'central', 'unrounded']},
            'ɛ': {'type': 'vowel', 'labels': ['open-mid', 'front', 'unrounded']},
            'ɜ': {'type': 'vowel', 'labels': ['open-mid', 'central', 'unrounded']},
            'ɞ': {'type': 'vowel', 'labels': ['open-mid', 'central', 'rounded']},
            'o': {'type': 'vowel', 'labels': ['close-mid', 'back', 'rounded']},
            'ø': {'type': 'vowel', 'labels': ['close-mid', 'front', 'rounded']},
            'ɵ': {'type': 'vowel', 'labels': ['close-mid', 'central', 'rounded']},
            'ɔ': {'type': 'vowel', 'labels': ['open-mid', 'back', 'rounded']},
            'œ': {'type': 'vowel', 'labels': ['open-mid', 'front', 'rounded']},
            'a': {'type': 'vowel', 'labels': ['open', 'front', 'unrounded']},
            'ɑ': {'type': 'vowel', 'labels': ['open', 'back', 'unrounded']},
            'ɐ': {'type': 'vowel', 'labels': ['near-open', 'central']},
            'ɒ': {'type': 'vowel', 'labels': ['open', 'back', 'rounded']},
            'æ': {'type': 'vowel', 'labels': ['near-open', 'front', 'unrounded']},
            'ɶ': {'type': 'vowel', 'labels': ['open', 'front', 'rounded']},
            'u': {'type': 'vowel', 'labels': ['close', 'back', 'rounded']},
            'ɯ': {'type': 'vowel', 'labels': ['close', 'back', 'unrounded']},
            'ʊ': {'type': 'vowel', 'labels': ['near-close', 'near-back', 'rounded']},
            'ʌ': {'type': 'vowel', 'labels': ['open-mid', 'back', 'unrounded']},
            'ɤ': {'type': 'vowel', 'labels': ['close-mid', 'back', 'unrounded']},

            # --- CLEAN DIACRITICS ---
            'ˈ': {'type': 'diacritic', 'labels': ['primary stress']},
            'ˌ': {'type': 'diacritic', 'labels': ['secondary stress']},
            'ː': {'type': 'diacritic', 'labels': ['long']},
            'ˑ': {'type': 'diacritic', 'labels': ['half-long']},
            'ʼ': {'type': 'diacritic', 'labels': ['ejective']},
            '˘': {'type': 'diacritic', 'labels': ['extra-short']},
            '̥': {'type': 'diacritic', 'labels': ['voiceless']},
            '̬': {'type': 'diacritic', 'labels': ['voiced']},
            'ʰ': {'type': 'diacritic', 'labels': ['aspirated']},
            '̹': {'type': 'diacritic', 'labels': ['more rounded']},
            '̜': {'type': 'diacritic', 'labels': ['less rounded']},
            '̟': {'type': 'diacritic', 'labels': ['advanced']},
            '̠': {'type': 'diacritic', 'labels': ['retracted']},
            '̈': {'type': 'diacritic', 'labels': ['centralized']},
            '̽': {'type': 'diacritic', 'labels': ['mid-centralized']},
            '̩': {'type': 'diacritic', 'labels': ['syllabic']},
            '̯': {'type': 'diacritic', 'labels': ['non-syllabic']},
            '˞': {'type': 'diacritic', 'labels': ['rhoticity']},
            '̤': {'type': 'diacritic', 'labels': ['breathy voiced']},
            '̰': {'type': 'diacritic', 'labels': ['creaky voiced']},
            '̼': {'type': 'diacritic', 'labels': ['linguolabial']},
            '̪': {'type': 'diacritic', 'labels': ['dental']},
            '̺': {'type': 'diacritic', 'labels': ['apical']},
            '̻': {'type': 'diacritic', 'labels': ['laminal']},
            '̃': {'type': 'diacritic', 'labels': ['nasalized']},
            'ⁿ': {'type': 'diacritic', 'labels': ['nasal release']},
            'ˡ': {'type': 'diacritic', 'labels': ['lateral release']},
            'ʷ': {'type': 'diacritic', 'labels': ['labialized']},
            'ʲ': {'type': 'diacritic', 'labels': ['palatalized']},
            'ˠ': {'type': 'diacritic', 'labels': ['velarized']},
            'ˤ': {'type': 'diacritic', 'labels': ['pharyngealized']},
            '̴': {'type': 'diacritic', 'labels': ['velarized or pharyngealized']},
            '̚': {'type': 'diacritic', 'labels': ['no audible release']},
            '̋': {'type': 'diacritic', 'labels': ['extra high tone']},
            '́': {'type': 'diacritic', 'labels': ['high tone']},
            '̄': {'type': 'diacritic', 'labels': ['mid tone']},
            '̀': {'type': 'diacritic', 'labels': ['low tone']},
            '̏': {'type': 'diacritic', 'labels': ['extra low tone']},
            '̌': {'type': 'diacritic', 'labels': ['rising tone']},
            '̂': {'type': 'diacritic', 'labels': ['falling tone']},
            '᷄': {'type': 'diacritic', 'labels': ['high rising tone']},
            '᷅': {'type': 'diacritic', 'labels': ['low rising tone']},
            '᷈': {'type': 'diacritic', 'labels': ['rising-falling tone']},
            '͡': {'type': 'diacritic', 'labels': ['tie bar (above)']},
            '͜': {'type': 'diacritic', 'labels': ['tie bar (below)']},
            '̝': {'type': 'diacritic', 'labels': ['raised']},
            '̞': {'type': 'diacritic', 'labels': ['lowered']},
            '̘': {'type': 'diacritic', 'labels': ['advanced tongue root']},
            '̙': {'type': 'diacritic', 'labels': ['retracted tongue root']}
        }

    def query(self, search_term):
        clean_term = search_term.strip().lower()

        # Scenario 1: Exact IPA Symbol Match
        if clean_term in self.data:
            return self.data[clean_term]['labels']

        # Parse search descriptors
        search_words = clean_term.split()
        if not search_words:
            return []

        matches = []
        for symbol, info in self.data.items():
            labels = info['labels']

            # Check if ALL typed search terms exist anywhere inside the entry's labels
            if all(word in labels for word in search_words):
                matches.append(symbol)

        if matches:
            # If the search filters down to an exact singular item (e.g., 'voiced bilabial plosive')
            if len(matches) == 1:
                return matches[0]
            # If it's a broad category description (e.g., 'voiced'), return all matching items
            return matches

        return []


# --- Run Tests ---
if __name__ == "__main__":
    ipa = IPALookup()

    print("Query '2:", ipa.query('̙'))
    print("\nQuery '1':", ipa.query('voiced bilabial'))
    print("\nQuery 'voiced bilabial plosive':", ipa.query('voiced bilabial plosive'))
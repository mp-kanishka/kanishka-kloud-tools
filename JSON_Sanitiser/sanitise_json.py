import json
import spacy
from tqdm import tqdm
from collections import defaultdict

# Load the English language model
print("Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")

# Define parliamentary procedural words to filter out
PARLIAMENTARY_PROCEDURAL_WORDS = {
## Parliamentary Procedures

'absent', 'adjourn', 'adjourned', 'adjournment', 'agenda', 'amendment', 'amendments', 'assembly', 'bill', 'bills', 'briefing', 'business', 'clause', 'clauses', 'convention', 'debate', 'debated', 'debates', 'division', 'draft', 'filibuster', 'hansard', 'inquiry', 'legislation', 'legislative', 'legislator', 'legislature', 'motion', 'motions', 'parliament', 'parliamentary', 'portfolio', 'presiding', 'privilege', 'procedure', 'procedures', 'proceedings', 'process', 'processes', 'provision', 'provisions', 'quorum', 'reading', 'readings', 'recess', 'recommendation', 'recommendations', 'resolution', 'resolutions', 'ruling', 'rulings', 'scrutiny', 'second', 'session', 'sessions', 'sitting', 'sittings', 'standing', 'table', 'tabled', 'tabling', 'terms', 'vote', 'votes',

## Parliamentary Roles and Titles

'backbench', 'backbencher', 'backbenchers', 'bench', 'cabinet', 'chair', 'chairman', 'chairperson', 'chairs', 'clerk', 'colleague', 'colleagues', 'committee', 'committees', 'constituency', 'constituents', 'councilor', 'deputy', 'electorate', 'excellency', 'frontbench', 'gentleman', 'gentlemen', 'hon', 'honorable', 'honourable', 'house', 'lady', 'ladies', 'lordship', 'madam', 'madame', 'member', 'members', 'minister', 'ministerial', 'ministers', 'mp', 'mps', 'official', 'officials', 'opposition', 'parliamentarian', 'parliamentarians', 'prime', 'representative', 'representatives', 'rt', 'secretary', 'secretaries', 'speaker', 'speakers', 'spokesperson', 'whip', 'whips', 'mr', 'ms', 'miss', 'mrs', 'sir', 'madam',

## Parliamentary Actions

'abstain', 'abstained', 'abstaining', 'address', 'addressed', 'addressing', 'adjourns', 'amend', 'amended', 'amending', 'appeal', 'appealed', 'appealing', 'appoint', 'appointed', 'appointing', 'approve', 'approved', 'approving', 'ask', 'asked', 'asking', 'assent', 'assented', 'assenting', 'assert', 'asserted', 'asserting', 'authorize', 'authorized', 'authorizing', 'brief', 'briefed', 'briefing', 'bring', 'bringing', 'brings', 'brought', 'call', 'called', 'calling', 'calls', 'carried', 'carry', 'carrying', 'chair', 'chaired', 'chairing', 'chairs', 'cite', 'cited', 'citing', 'commence', 'commenced', 'commencing', 'commend', 'commended', 'commending', 'concur', 'concurred', 'concurring', 'consider', 'considered', 'considering', 'consult', 'consulted', 'consulting', 'convene', 'convened', 'convening', 'debate', 'debated', 'debating', 'decide', 'decided', 'deciding', 'declare', 'declared', 'declaring', 'defer', 'deferred', 'deferring', 'delegate', 'delegated', 'delegating', 'deliberate', 'deliberated', 'deliberating', 'demand', 'demanded', 'demanding', 'designate', 'designated', 'designating', 'direct', 'directed', 'directing', 'disallow', 'disallowed', 'disallowing', 'discharge', 'discharged', 'discharging', 'discuss', 'discussed', 'discussing', 'dispatch', 'dispatched', 'dispatching', 'dissent', 'dissented', 'dissenting', 'elect', 'elected', 'electing', 'enact', 'enacted', 'enacting', 'enforce', 'enforced', 'enforcing', 'examine', 'examined', 'examining', 'exclude', 'excluded', 'excluding', 'extend', 'extended', 'extending', 'formulate', 'formulated', 'formulating', 'forward', 'forwarded', 'forwarding', 'grant', 'granted', 'granting', 'move', 'moved', 'moving', 'nominate', 'nominated', 'nominating', 'notify', 'notified', 'notifying', 'object', 'objected', 'objecting', 'offer', 'offered', 'offering', 'open', 'opened', 'opening', 'order', 'ordered', 'ordering', 'pass', 'passed', 'passing', 'permit', 'permiting', 'place', 'placed', 'plan', 'prepared', 'preparing', 'prescribe', 'prescribed', 'prescribing', 'present', 'presented', 'presenting', 'preside', 'presided', 'presiding', 'proceed', 'proceeded', 'proceeding', 'prohibit', 'prohibited', 'prohibiting', 'promise', 'promised', 'promising', 'promote', 'proposed', 'proposing', 'protect', 'protected', 'protecting', 'provide', 'provided', 'providing', 'publish', 'published', 'putting', 'question', 'quoted', 'quoting', 'raise', 'raised', 'raising', 'ratify', 'read', 'receive', 'received', 'receiving', 'recommend', 'record', 'refer', 'register', 'reiterate', 'release', 'relieve', 'remain', 'remind', 'remove', 'render', 'renew', 'reply', 'report', 'represent', 'request', 'require', 'rescind', 'reserve', 'resign', 'resolve', 'respond', 'resume', 'retain', 'return', 'review', 'revise', 'revoke', 'rule', 'schedule', 'seek', 'select', 'set', 'sign', 'signed', 'signing', 'specify', 'state', 'submit', 'suggest', 'summon', 'supply', 'support', 'suspend', 'table', 'take', 'taken', 'taking', 'terminate', 'testify', 'transact', 'transfer', 'transmit', 'try', 'trying', 'undergo', 'undertake', 'update', 'uphold', 'urge', 'validate', 'witness', 'write', 'yield', 'apply', 'allocate', 'conduct', 'deliver', 'handle',

## General Governance and Policy

'action', 'actions', 'agenda', 'agendas', 'allocation', 'allocations', 'amendment', 'amendments', 'announcement', 'announcements', 'annual', 'appointment', 'appointments', 'approach', 'approaches', 'authorization', 'authorizations', 'case', 'cases', 'category', 'categories', 'cause', 'causes', 'central', 'certification', 'certifications', 'challenge', 'challenges', 'channel', 'channels', 'charge', 'charges', 'circumstance', 'circumstances', 'claim', 'claims', 'classification', 'classifications', 'clause', 'clauses', 'code', 'codes', 'collection', 'collections', 'comment', 'comments', 'commission', 'commissions', 'commitment', 'commitments', 'committee', 'committees', 'common', 'communication', 'communications', 'community', 'communities', 'competitive', 'compliance', 'component', 'components', 'concern', 'concerns', 'conclusion', 'conclusions', 'condition', 'conditions', 'conduct', 'conference', 'conferences', 'confidence', 'configuration', 'configurations', 'connection', 'connections', 'consensus', 'consequence', 'consequences', 'consideration', 'considerations', 'consultation', 'consultations', 'contribution', 'contributions', 'control', 'controls', 'cooperation', 'core', 'correspondence', 'counterpart', 'counterparts', 'coverage', 'coverages', 'creation', 'creations', 'credential', 'credentials', 'criteria', 'criterion', 'critical', 'criticism', 'criticisms', 'current', 'deal', 'deals', 'decision', 'decisions', 'declaration', 'declarations', 'decrease', 'decreases', 'deficit', 'deficits', 'definition', 'definitions', 'delay', 'delays', 'delegation', 'delegations', 'delivery', 'deliveries', 'demand', 'demands', 'department', 'departments', 'detail', 'details', 'determination', 'determinations', 'development', 'developments', 'difference', 'differences', 'difficulty', 'difficulties', 'direction', 'directions', 'directive', 'directives', 'disciplines', 'disclosure', 'disclosures', 'discretion', 'discussion', 'discussions', 'disorder', 'disorders', 'dispute', 'disputes', 'district', 'districts', 'division', 'divisions', 'document', 'documents', 'domain', 'domains', 'draft', 'drafts', 'effect', 'effects', 'effort', 'efforts', 'element', 'elements', 'enterprise', 'enterprises', 'equipment', 'equity', 'estimate', 'estimates', 'evaluation', 'evaluations', 'event', 'events', 'examination', 'examinations', 'example', 'examples', 'exception', 'exceptions', 'exchange', 'exchanges', 'executive', 'executives', 'exemption', 'exemptions', 'exercise', 'exercises', 'expectation', 'expectations', 'expenditure', 'expenditures', 'expense', 'expenses', 'experience', 'experiences', 'experiment', 'experiments', 'expert', 'experts', 'explanation', 'explanations', 'extension', 'extensions', 'facility', 'field', 'fields', 'figure', 'figures', 'file', 'files', 'filing', 'filings', 'focus', 'focuses', 'force', 'forces', 'form', 'forms', 'formula', 'formulas', 'framework', 'frameworks', 'function', 'functions', 'fund', 'funds', 'funding', 'future', 'gain', 'gains', 'gap', 'gaps', 'general', 'goal', 'goals', 'goods', 'governance', 'government', 'governments', 'governor', 'governors', 'grant', 'grants', 'group', 'groups', 'guidance', 'guideline', 'guidelines', 'hearing', 'hearings', 'impact', 'impacts', 'implementation', 'implementations', 'implication', 'implications', 'increase', 'increases', 'indication', 'indications', 'initiative', 'initiatives', 'instance', 'instances', 'institution', 'institutions', 'instruction', 'instructions', 'instrument', 'instruments', 'integration', 'integrations', 'intentions', 'interaction', 'interactions', 'interface', 'interfaces', 'interpretation', 'interpretations', 'intervention', 'interventions', 'interview', 'interviews', 'introduction', 'introductions', 'invitation', 'invitations', 'involvement', 'involvements', 'issue', 'issues', 'item', 'items', 'key', 'label', 'labels', 'language', 'languages', 'law', 'laws', 'league', 'leagues', 'legal', 'legislation', 'legislations', 'legislature', 'legislatures', 'letter', 'letters', 'level', 'levels', 'liability', 'liabilities', 'license', 'licenses', 'limitation', 'limitations', 'line', 'lines', 'link', 'links', 'list', 'lists', 'location', 'locations', 'lot', 'lots', 'maintenance', 'management', 'mandate', 'mandates', 'manual', 'manuals', 'margin', 'margins', 'matter', 'matters', 'maximum', 'measure', 'measures', 'mechanism', 'mechanisms', 'media', 'member', 'members', 'membership', 'memberships', 'memorandum', 'memoranda', 'message', 'messages', 'method', 'methods', 'minister', 'ministers', 'ministry', 'ministries', 'mistake', 'mistakes', 'mode', 'modes', 'model', 'models', 'modification', 'modifications', 'module', 'modules', 'monitoring', 'motion', 'motions', 'movement', 'movements', 'multiple', 'municipal', 'name', 'names', 'nation', 'necessity', 'necessities', 'need', 'needs', 'network', 'networks', 'nomination', 'nominations', 'normal', 'norms', 'note', 'notes', 'notice', 'notices', 'notification', 'notifications', 'notion', 'notions', 'number', 'numbers', 'objection', 'objections', 'objective', 'objectives', 'observation', 'observations', 'occasion', 'occasions', 'offer', 'offers', 'office', 'offices', 'official', 'officials', 'omission', 'omissions', 'open', 'opens', 'operation', 'operations', 'opinion', 'opinions', 'opposition', 'option', 'options', 'orders', 'organization', 'organizations', 'outcome', 'outcomes', 'output', 'outputs', 'overview', 'overviews', 'page', 'pages', 'paper', 'papers', 'paragraph', 'paragraphs', 'parameter', 'parameters', 'parliament', 'parliaments', 'part', 'parts', 'participant', 'participants', 'participation', 'party', 'parties', 'passage', 'passages', 'past', 'path', 'paths', 'pattern', 'patterns', 'payments', 'percent', 'percentage', 'percentages', 'perception', 'perceptions', 'period', 'periods', 'permission', 'permissions', 'person', 'persons', 'perspective', 'perspectives', 'phase', 'phases', 'physical', 'platform', 'platforms', 'point', 'points', 'political', 'position', 'positions', 'possibility', 'possibilities', 'practice', 'practices', 'precedent', 'precedents', 'predecessor', 'predecessors', 'prediction', 'predictions', 'preference', 'preferences', 'premise', 'premises', 'presence', 'presentation', 'presentations', 'pressure', 'pressures', 'prevention', 'preventions', 'principle', 'principles', 'priority', 'priorities', 'procedure', 'procedures', 'process', 'processes', 'production', 'productions', 'profession', 'professions', 'proposal', 'proposals', 'protection', 'protections', 'protocol', 'protocols', 'provision', 'provisions', 'public', 'publics', 'publication', 'publications', 'purpose', 'purposes', 'qualification', 'qualifications', 'quality', 'qualities', 'quantity', 'quantities', 'question', 'questions', 'range', 'ranges', 'rank', 'ranks', 'rate', 'rates', 'ratio', 'ratios', 'reaction', 'reactions', 'reason', 'reasons', 'receipt', 'receipts', 'reception', 'receptions', 'recognition', 'recognitions', 'recommendation', 'recommendations', 'record', 'records', 'recovery', 'recoveries', 'reduction', 'reductions', 'reference', 'references', 'relevance', 'remark', 'remarks', 'remedy', 'remedies', 'reminder', 'reminders', 'removal', 'removals', 'renewal', 'renewals', 'replacement', 'replacements', 'reply', 'replies', 'representation', 'representations', 'representative', 'representatives', 'republic', 'republics', 'request', 'requests', 'requirement', 'requirements', 'resolution', 'resolutions', 'resource', 'resources', 'response', 'responses', 'responsibility', 'responsibilities', 'restriction', 'restrictions', 'result', 'results', 'retirement', 'retirements', 'return', 'returns', 'review', 'reviews', 'revision', 'revisions', 'scope', 'scopes', 'score', 'scores', 'sector', 'sectors', 'security', 'securities', 'selection', 'selections', 'sense', 'senses', 'sensitivity', 'sensitivities', 'sentence', 'sentences', 'separation', 'separations', 'sequence', 'sequences', 'series', 'session', 'sessions', 'set', 'sets', 'setting', 'settings', 'settlement', 'settlements', 'severity', 'severities', 'share', 'shares', 'shift', 'shifts', 'shortage', 'shortages', 'side', 'sides', 'sign', 'signs', 'signal', 'signals', 'significance', 'significances', 'similarity', 'similarities', 'simplicity', 'simplicities', 'situation', 'situations', 'size', 'sizes', 'solution', 'solutions', 'source', 'sources', 'space', 'spaces', 'speaker', 'speakers', 'specialist', 'specialists', 'specification', 'specifications', 'specificity', 'specificities', 'speech', 'speeches', 'spending', 'spendings', 'stability', 'stabilities', 'stage', 'stages', 'stakeholder', 'stakeholders', 'standard', 'standards', 'state', 'states', 'statement', 'statements', 'status', 'statuses', 'statute', 'statutes', 'subject', 'subjects', 'submission', 'submissions', 'subsection', 'subsections', 'subsidiary', 'subsidiaries', 'substance', 'substances', 'suggestion', 'suggestions', 'summary', 'summaries', 'supervision', 'supervisions', 'supervisor', 'supervisors', 'table', 'tables', 'target', 'targets', 'task', 'tasks', 'team', 'teams', 'term', 'terms', 'time', 'times', 'title', 'titles', 'topic', 'topics', 'total', 'totals', 'type', 'types', 'unit', 'units', 'unities', 'use', 'uses', 'user', 'users', 'validity', 'validities', 'variation', 'variations', 'variety', 'varieties', 'verification', 'verifications', 'version', 'versions', 'way', 'ways', 'choices',


}

# Define words that should never be removed, regardless of NLP rules
DO_NOT_REMOVE = {
    'make',
    'ftse',  # Stock market index that should be preserved

    # Add more words that should never be removed here
}

# Cache for spaCy analysis results
spacy_cache = {}

def clean_word(word):
    """Clean a word by removing punctuation and converting to lowercase."""
    word = word.lower()
    word = ''.join(c for c in word if c.isalnum())
    return word

def analyze_words_batch(words, batch_size=1000):
    """Analyze a batch of words using spaCy."""
    # Filter out words we've already analyzed
    words_to_analyze = [w for w in words if w not in spacy_cache]
    if not words_to_analyze:
        return
    
    # Process words in batches
    for i in range(0, len(words_to_analyze), batch_size):
        batch = words_to_analyze[i:i + batch_size]
        docs = list(nlp.pipe(batch))
        for word, doc in zip(batch, docs):
            if doc:
                token = doc[0]
                spacy_cache[word] = {
                    'is_stop': token.is_stop,
                    'pos': token.pos_
                }

def should_keep_word(word):
    """Determine if a word should be kept based on spaCy's analysis."""
    # Clean the word first
    cleaned = clean_word(word)
    if not cleaned:  # Empty string
        return False
    if len(cleaned) <= 1:  # Single characters
        return False
    if cleaned.isnumeric():  # Numbers
        return False
    
    # Debug logging for 'ftse'
    if cleaned == 'ftse':
        print(f"Processing word 'ftse': cleaned='{cleaned}'")
        print(f"in PARLIAMENTARY_PROCEDURAL_WORDS={cleaned in PARLIAMENTARY_PROCEDURAL_WORDS}")
        print(f"in DO_NOT_REMOVE={cleaned in DO_NOT_REMOVE}")
    
    # Check if the word is in the parliamentary procedural words set first
    if cleaned in PARLIAMENTARY_PROCEDURAL_WORDS:
        return False
    
    # Check if the word is in the do not remove list
    if cleaned in DO_NOT_REMOVE:
        return True
    
    # Get cached spaCy analysis or analyze the word
    if cleaned not in spacy_cache:
        analyze_words_batch([cleaned])
    
    if cleaned not in spacy_cache:
        return False
    
    analysis = spacy_cache[cleaned]
    
    # Debug logging for 'ftse' part 2
    if cleaned == 'ftse':
        print(f"spaCy analysis: is_stop={analysis['is_stop']}, pos={analysis['pos']}")
    
    # For verbs, check if the base form is in our exclusion list
    if analysis['pos'] == 'VERB':
        # Get the base form of the verb
        base_form = cleaned.rstrip('s')  # Remove trailing 's' for basic verb forms
        if base_form in PARLIAMENTARY_PROCEDURAL_WORDS:
            return False
    
    # Filter out common parts of speech we want to exclude
    excluded_pos = {
        #'NOUN',      # Common nouns
        #'PROPN',     # Proper nouns
        'ADJ',       # Adjectives
        'ADV',       # Adverbs
        'PRON',      # Pronouns
        'DET',       # Determiners
        'NUM',       # Numbers
        'AUX',       # Auxiliary verbs
        'PART',      # Particles
    }
    
    # Filter out stop words and common parts of speech
    if analysis['is_stop'] or analysis['pos'] in excluded_pos:
        return False
        
    return True

try:
    # Read the original JSON file
    print("Reading JSON file...")
    with open('combined_speaker_statistics.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Collect all unique words first
    print("Collecting unique words...")
    all_words = set()
    for speaker_data in data.values():
        all_words.update(speaker_data.get("word_counts", {}).keys())
    
    # Pre-analyze all words in batches
    print("Pre-analyzing words with spaCy...")
    analyze_words_batch(list(all_words))
    
    # Process the data
    print("Processing speakers...")
    cleaned_data = {}
    for speaker in tqdm(data.keys(), desc="Processing speakers"):
        speaker_data = data[speaker]
        # Copy the speaker's metadata
        cleaned_data[speaker] = {
            "person_id": speaker_data["person_id"],
            "total_speeches": speaker_data["total_speeches"],
            "word_counts": {}
        }
        
        # Only clean the word_counts section
        word_counts = speaker_data.get("word_counts", {})
        cleaned_words = {
            word: count for word, count in word_counts.items()
            if should_keep_word(word)
        }
        cleaned_data[speaker]["word_counts"] = cleaned_words

    # Save the cleaned data
    print("Saving cleaned data...")
    output_file = 'cleaned_speaker_statistics.json'
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(cleaned_data, file, indent=2, ensure_ascii=False)
    
    print(f"Successfully cleaned the JSON data. Output saved to {output_file}")
    
except Exception as e:
    print(f"An error occurred: {str(e)}") 
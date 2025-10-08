
"""
Tech Trends Harvester - Utility Functions
Author: Rich Lewis
"""

import re, statistics, datetime as dt
import functools
import traceback

# Common browser user-agent
# Using a recent Chrome on Windows (most common)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Expanded stop words - common English words that aren't tech-relevant
STOP = set('the a an and or of for to in on with without from by is are was were as at it this that be have has had not can will just into about over under out up down off more most other such its their our your you they them their there here where when what why how who whom whose which these those then than this these there\'s here\'s where\'s what\'s who\'s that\'s it\'s he\'s she\'s we\'re they\'re you\'re i\'m'.split())

# Common system/infrastructure terms that aren't blog-worthy
BORING_TERMS = set([
    # Linux/Unix basics
    'linux', 'unix', 'bash', 'shell', 'sudo', 'root', 'usr', 'bin', 'lib', 'libc', 'glibc',
    'kernel', 'systemd', 'daemon', 'cron', 'pipe', 'file', 'dir', 'path', 'home', 'tmp',
    # Generic programming terms
    'function', 'method', 'class', 'variable', 'string', 'int', 'float', 'bool', 'array',
    'list', 'dict', 'map', 'set', 'object', 'type', 'null', 'none', 'true', 'false',
    'error', 'warning', 'info', 'debug', 'log', 'print', 'test', 'tests', 'testing',
    # Generic tech words
    'http', 'https', 'html', 'css', 'json', 'xml', 'yaml', 'csv', 'txt', 'pdf',
    'file', 'folder', 'directory', 'path', 'url', 'uri', 'api', 'rest', 'soap',
    # Common filler words in titles
    'using', 'with', 'without', 'how', 'what', 'why', 'when', 'where', 'guide', 
    'tutorial', 'introduction', 'getting', 'started', 'made', 'simple', 'easy',
    'best', 'good', 'better', 'great', 'awesome', 'amazing', 'quick', 'fast',
    'new', 'old', 'latest', 'updated', 'release', 'version', 'build', 'update',
    # Time/date words
    'today', 'yesterday', 'tomorrow', 'week', 'month', 'year', 'day', 'time',
    # Meta words
    'post', 'blog', 'article', 'write', 'read', 'show', 'tell', 'ask', 'hn',
    'comments', 'comment', 'discussion', 'thread', 'reply', 'vote', 'votes',
    # Numbers and common short words
    'one', 'two', 'three', 'first', 'second', 'third', 'last', 'next', 'prev',
])

# Terms that ARE interesting for tech blogs (allowlist approach for common terms)
INTERESTING_TECH = set([
    # Hot frameworks/languages
    'react', 'vue', 'svelte', 'angular', 'nextjs', 'next.js', 'nuxt', 'remix',
    'rust', 'golang', 'python', 'typescript', 'javascript', 'kotlin', 'swift',
    # AI/ML buzzwords
    'ai', 'ml', 'llm', 'gpt', 'openai', 'anthropic', 'claude', 'chatgpt', 'gemini',
    'llama', 'mistral', 'transformer', 'embedding', 'rag', 'langchain', 'langgraph',
    'pytorch', 'tensorflow', 'keras', 'scikit-learn', 'huggingface',
    # Cloud/infra
    'kubernetes', 'k8s', 'docker', 'aws', 'azure', 'gcp', 'cloudflare', 'vercel',
    'terraform', 'ansible', 'jenkins', 'github-actions', 'gitlab-ci',
    # Databases
    'postgres', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra',
    'mysql', 'mariadb', 'sqlite', 'dynamodb', 'firestore', 'supabase',
    # Modern tools/platforms
    'vscode', 'cursor', 'copilot', 'github', 'gitlab', 'bitbucket',
    'slack', 'discord', 'notion', 'obsidian', 'raycast',
])

def now_iso():
    return dt.datetime.utcnow().isoformat() + 'Z'

def tokenize_title(title: str, min_length=3):
    """
    Extract meaningful terms from a title, filtering out noise.
    
    Args:
        title: The title to tokenize
        min_length: Minimum term length (default 3, but 4+ is better for blog topics)
    
    Returns:
        List of cleaned, relevant terms
    """
    words = re.findall(r"[A-Za-z0-9_\-\+\.]{3,}", title.lower())
    
    result = []
    for w in words:
        w = w.strip('.').strip('-').strip('_')
        
        # Skip if in stop words or too short
        if w in STOP or len(w) < min_length:
            continue
        
        # Skip boring infrastructure terms UNLESS they're in the interesting list
        if w in BORING_TERMS and w not in INTERESTING_TECH:
            continue
        
        # Skip pure numbers
        if w.isdigit():
            continue
        
        # Skip single letters (unless it's a known tech term like 'k8s')
        if len(w) == 1:
            continue
        
        # Prefer longer, more specific terms (4+ chars are usually more meaningful)
        if len(w) >= 4 or w in INTERESTING_TECH:
            result.append(w)
    
    return result

def is_interesting_term(term: str) -> bool:
    """
    Determine if a term is interesting enough for a blog post.
    
    Criteria:
    - Not in boring list
    - In interesting list OR long enough to be specific (5+ chars)
    - Looks like a product/technology name (mixed case, dash-separated, etc.)
    """
    term_lower = term.lower()
    
    # Explicit interesting list
    if term_lower in INTERESTING_TECH:
        return True
    
    # Explicitly boring
    if term_lower in BORING_TERMS:
        return False
    
    # Short generic words are usually boring
    if len(term) < 5:
        return False
    
    # Looks like a product name (CamelCase, kebab-case, etc.)
    if '-' in term or '_' in term or any(c.isupper() for c in term[1:]):
        return True
    
    # Long enough to be specific
    if len(term) >= 6:
        return True
    
    return False

def extract_phrases(text: str, min_words=2, max_words=5) -> list:
    """
    Extract meaningful phrases (n-grams) from text instead of individual words.
    
    This is CRITICAL: "react tutorial for beginners" is a blog topic.
    "react" alone is not.
    
    Args:
        text: Input text (title, description, etc.)
        min_words: Minimum words per phrase (default 2)
        max_words: Maximum words per phrase (default 5)
    
    Returns:
        List of phrases
    """
    # Clean and tokenize
    words = re.findall(r"[A-Za-z0-9_\-\+\.]+", text.lower())
    words = [w for w in words if w not in STOP and len(w) >= 3]
    
    phrases = []
    
    # Generate n-grams (2-5 word phrases)
    for n in range(min_words, min(max_words + 1, len(words) + 1)):
        for i in range(len(words) - n + 1):
            phrase = " ".join(words[i:i+n])
            
            # Skip if too many boring terms
            phrase_words = phrase.split()
            boring_count = sum(1 for w in phrase_words if w in BORING_TERMS)
            if boring_count > len(phrase_words) / 2:
                continue
            
            phrases.append(phrase)
    
    return phrases

def is_question(text: str) -> bool:
    """
    Check if text is a question.
    Questions are SEO GOLD - they have clear intent!
    """
    text_lower = text.lower().strip()
    
    # Check for question mark
    if '?' in text:
        return True
    
    # Check for question words at start
    question_words = [
        'how', 'what', 'why', 'when', 'where', 'who', 'which',
        'can', 'could', 'should', 'would', 'will', 'is', 'are',
        'does', 'do', 'did', 'has', 'have', 'had'
    ]
    
    first_word = text_lower.split()[0] if text_lower.split() else ""
    return first_word in question_words

def extract_question_intent(text: str) -> str:
    """
    Extract the type of question for content format guidance.
    
    Returns: "how-to", "what-is", "comparison", "best", "tutorial", "unknown"
    """
    text_lower = text.lower()
    
    if any(x in text_lower for x in ['how to', 'how do', 'how can', 'how does']):
        return "how-to"
    
    if any(x in text_lower for x in ['what is', 'what are', 'what does']):
        return "what-is"
    
    if any(x in text_lower for x in [' vs ', ' versus ', 'compared to', 'difference between']):
        return "comparison"
    
    if any(x in text_lower for x in ['best ', 'top ', 'better than']):
        return "best"
    
    if any(x in text_lower for x in ['tutorial', 'guide', 'learn', 'getting started']):
        return "tutorial"
    
    if any(x in text_lower for x in ['why ', 'when ', 'where ']):
        return "explainer"
    
    return "unknown"

def score_blog_worthiness(text: str, metrics: dict = None) -> float:
    """
    Score how blog-worthy a topic is based on multiple signals.
    
    Args:
        text: The topic/title
        metrics: Dict with optional keys like 'search_volume', 'engagement', etc.
    
    Returns:
        Score (higher = better blog topic)
    """
    score = 0.0
    metrics = metrics or {}
    
    # Length bonus (2-6 words is sweet spot for blog titles)
    word_count = len(text.split())
    if 2 <= word_count <= 6:
        score += 2.0
    elif word_count > 6:
        score += 0.5
    
    # Question bonus (questions have clear intent)
    if is_question(text):
        score += 3.0
    
    # Specific format bonuses
    intent = extract_question_intent(text)
    intent_scores = {
        "how-to": 2.5,
        "comparison": 2.0,
        "tutorial": 2.0,
        "what-is": 1.5,
        "best": 1.5,
    }
    score += intent_scores.get(intent, 0)
    
    # Year bonus (2025, 2026 = fresh content)
    if any(year in text for year in ['2025', '2026']):
        score += 1.0
    
    # Interesting tech bonus
    text_lower = text.lower()
    interesting_count = sum(1 for tech in INTERESTING_TECH if tech in text_lower)
    score += interesting_count * 0.5
    
    # Search volume bonus (if available)
    if metrics.get('search_volume', 0) > 0:
        # Logarithmic scale (1000 searches = +2, 10000 = +3, etc.)
        import math
        score += math.log10(metrics['search_volume']) * 0.5
    
    # Engagement bonus (social proof)
    if metrics.get('engagement', 0) > 0:
        score += min(metrics['engagement'] / 100, 3.0)
    
    return score

def zscore(values):
    if not values: return []
    if len(values) == 1: return [0.0]
    mu = statistics.mean(values)
    sd = statistics.pstdev(values) or 1.0
    return [(v - mu) / sd for v in values]

def safe_fetch(func):
    """Decorator to add comprehensive error handling to collector functions."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result is None:
                return []
            return result
        except ConnectionError as e:
            print(f"[{func.__module__}] Connection error: {e}")
            return []
        except TimeoutError as e:
            print(f"[{func.__module__}] Timeout: {e}")
            return []
        except Exception as e:
            print(f"[{func.__module__}] Unexpected error: {e}")
            traceback.print_exc()
            return []
    return wrapper

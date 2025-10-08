
"""
Tech Trends Harvester - Data Aggregation and Scoring
Author: Rich Lewis
"""

import datetime as dt

import pandas as pd

from .util import zscore, is_interesting_term, is_question, extract_question_intent, score_blog_worthiness

def aggregate(rows, weights: dict, min_score_threshold=0.5):
    """
    Aggregate rows with weighted z-scores and filter out low-signal terms.

    Args:
        rows: List of row dicts from collectors
        weights: Dict of source -> weight multiplier
        min_score_threshold: Minimum score to include in results

    Returns:
        Tuple of (aggregated_rows, dataframe)
    """
    df = pd.DataFrame(rows)
    if df.empty:
        return [], pd.DataFrame()
    df['term'] = df['term'].str.strip().str.lower()
    df['group'] = df['source'] + '::' + df['metric_name']
    zs = []
    for g, gdf in df.groupby('group'):
        zs.extend(zscore(list(gdf['metric_value'])))
    df['z'] = zs
    df['weight'] = df['source'].map(weights).fillna(0.5)
    df['contrib'] = df['z'] * df['weight']
    agg = df.groupby('term').agg(
        score=('contrib','sum'),
        sources=('source', lambda s: sorted(set(s))),
        source_count=('source', 'nunique'),  # How many different sources mention it
    ).reset_index().sort_values('score', ascending=False)
    
    # Filter out low scores
    agg = agg[agg['score'] > min_score_threshold]
    
    top_signals = (df.sort_values(['term','contrib'], ascending=[True,False])
                     .groupby('term').head(4)[['term','source','metric_name','metric_value','url']])
    signals: dict[str, list] = {}
    for r in top_signals.to_dict(orient='records'):
        signals.setdefault(r['term'], []).append({
            'source': r['source'],
            'metric_name': r['metric_name'],
            'metric_value': int(r['metric_value']) if isinstance(r['metric_value'], (int,float)) else r['metric_value'],
            'url': r['url']
        })
    agg['top_signals'] = agg['term'].map(signals.get)
    return agg.to_dict(orient='records'), df

def get_blog_topics(agg_rows, top_n=50):
    """
    Filter aggregated results to get the most blog-worthy topics.
    
    NEW: Prioritizes questions and full phrases over individual words!
    
    Criteria:
    - Questions get huge bonus (clear intent)
    - Multi-word phrases preferred over single words
    - Must appear in multiple sources OR have very high engagement
    - Sorted by blog_worthiness score
    
    Returns:
        List of blog-worthy topic dicts with enriched metadata
    """
    blog_topics = []
    
    for row in agg_rows:
        term = row['term']
        score = row['score']
        source_count = row.get('source_count', 1)
        
        # Calculate blog worthiness using new scoring
        metrics = {
            'search_volume': row.get('search_volume', 0),
            'engagement': row.get('engagement', 0),
        }
        blog_score = score_blog_worthiness(term, metrics)
        
        # Questions and multi-word phrases get priority
        is_q = is_question(term)
        word_count = len(term.split())
        
        # Skip if single word AND not interesting AND low score
        if word_count == 1 and not is_interesting_term(term) and blog_score < 3.0:
            continue
        
        # Questions always pass (they're gold!)
        if not is_q:
            # Non-questions need validation
            if source_count < 2 and blog_score < 5.0:
                continue
            
            # Multi-word phrases are usually good
            if word_count < 2 and not is_interesting_term(term):
                continue
        
        # Add enriched metadata
        enriched = row.copy()
        enriched['blog_worthiness'] = blog_score + (score * 0.5)  # Combine both scores
        enriched['category'] = categorize_term(term)
        enriched['is_question'] = is_q
        enriched['question_type'] = extract_question_intent(term) if is_q else None
        enriched['word_count'] = word_count
        
        blog_topics.append(enriched)
    
    # Sort by blog worthiness
    blog_topics.sort(key=lambda x: x['blog_worthiness'], reverse=True)
    
    return blog_topics[:top_n]

def categorize_term(term: str) -> str:
    """Categorize a term for easier browsing."""
    term_lower = term.lower()
    
    # AI/ML
    if any(x in term_lower for x in ['ai', 'ml', 'llm', 'gpt', 'model', 'neural', 'learning', 'transformer']):
        return 'AI/ML'
    
    # Cloud/DevOps
    if any(x in term_lower for x in ['kubernetes', 'k8s', 'docker', 'cloud', 'aws', 'azure', 'gcp', 'deploy', 'cicd']):
        return 'Cloud/DevOps'
    
    # Frontend
    if any(x in term_lower for x in ['react', 'vue', 'svelte', 'angular', 'css', 'frontend', 'ui', 'component']):
        return 'Frontend'
    
    # Backend/API
    if any(x in term_lower for x in ['api', 'backend', 'server', 'graphql', 'rest', 'microservice']):
        return 'Backend'
    
    # Database
    if any(x in term_lower for x in ['database', 'postgres', 'mongo', 'sql', 'nosql', 'redis', 'elastic']):
        return 'Database'
    
    # Languages
    if any(x in term_lower for x in ['rust', 'golang', 'python', 'javascript', 'typescript', 'java', 'kotlin']):
        return 'Language'
    
    # Tools/IDE
    if any(x in term_lower for x in ['vscode', 'cursor', 'git', 'github', 'editor', 'copilot']):
        return 'Tools'
    
    # Security
    if any(x in term_lower for x in ['security', 'auth', 'oauth', 'jwt', 'encrypt', 'ssl', 'tls']):
        return 'Security'
    
    return 'Tech'

def compute_movers(prev_rows, curr_rows, top_n=50):
    prev = {r['term']: r for r in (prev_rows or [])}
    movers = []
    for r in curr_rows:
        term = r['term']
        score = float(r['score'])
        p = prev.get(term, {})
        prev_score = float(p.get('score', 0.0) or 0.0)
        delta = score - prev_score
        pct = (delta / abs(prev_score)) * 100.0 if prev_score else 0.0
        movers.append({
            'term': term,
            'score_now': score,
            'score_prev': prev_score,
            'delta': delta,
            'pct': pct,
            'sources': r.get('sources', [])
        })
    movers.sort(key=lambda x: abs(x['delta']), reverse=True)
    return movers[:top_n]

def as_markdown(agg_rows, by_source_rows, movers_rows=None):
    lines = []
    lines.append("# Tech Trends Report\n")
    lines.append(f"_Generated: {dt.datetime.utcnow().isoformat()}Z_\n")
    if movers_rows:
        lines.append("## Movers (WoW)\n")
        lines.append("| # | Term | Δ | Δ% | Now | Prev | Sources |")
        lines.append("|---:|---|---:|---:|---:|---:|---|")
        for i, r in enumerate(movers_rows, 1):
            sources = ", ".join(r.get('sources', []))
            lines.append(f"| {i} | {r['term']} | {r['delta']:.3f} | {r['pct']:.1f}% | {r['score_now']:.3f} | {r['score_prev']:.3f} | {sources} |")
        lines.append("")
    lines.append("## Aggregated Ranking\n")
    lines.append("| # | Term | Score | Sources | Top signals |")
    lines.append("|---:|---|---:|---|---|")
    for i, r in enumerate(agg_rows, 1):
        sources = ", ".join(r.get('sources', []))
        sigs = "; ".join([f"{s['source']} {s['metric_name']}={s['metric_value']}" for s in (r.get('top_signals') or [])])
        lines.append(f"| {i} | {r['term']} | {r['score']:.3f} | {sources} | {sigs} |")
    lines.append("\n## By Source\n")
    for src, rows in sorted(by_source_rows.items()):
        lines.append(f"### {src}\n")
        lines.append("| Term | Kind | Metric | Value | Link |")
        lines.append("|---|---|---|---:|---|")
        for row in rows[:200]:
            lines.append(f"| {row['term']} | {row.get('kind','')} | {row.get('metric_name','')} | {row.get('metric_value',0)} | [{row.get('url','')}]({row.get('url','')}) |")
        lines.append("")
    return "\n".join(lines)

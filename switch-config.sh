#!/usr/bin/env bash
#
# Switch between production and testing configurations
#

set -e

CONFIG_DIR="config"
CURRENT="$CONFIG_DIR/sources.yaml"
PRODUCTION="$CONFIG_DIR/sources-production.yaml"
TESTING="$CONFIG_DIR/sources-testing.yaml"

show_usage() {
    echo "Usage: ./switch-config.sh [testing|production|status]"
    echo ""
    echo "Commands:"
    echo "  testing     - Switch to safe testing config (Google Trends disabled)"
    echo "  production  - Switch to production config (all sources enabled)"
    echo "  status      - Show which config is currently active"
    echo ""
    echo "Examples:"
    echo "  ./switch-config.sh testing      # Safe for rapid testing"
    echo "  ./switch-config.sh production   # Full data collection"
    echo "  ./switch-config.sh status       # Check current config"
}

show_status() {
    if [ -f "$CURRENT" ]; then
        if grep -q "enabled: false.*Google Trends" "$CURRENT" 2>/dev/null || \
           grep -q "google_trends:" "$CURRENT" | head -5 | grep -q "enabled: false"; then
            echo "[STATUS] Current config: TESTING (Google Trends disabled)"
        else
            echo "[STATUS] Current config: PRODUCTION (all sources enabled)"
        fi
        
        echo ""
        echo "Source status:"
        echo "  Google Trends: $(grep -A 1 'google_trends:' "$CURRENT" | grep 'enabled:' | awk '{print $2}')"
        echo "  GitHub Trending: $(grep -A 1 'github_trending:' "$CURRENT" | grep 'enabled:' | awk '{print $2}')"
        echo "  Reddit Posts: $(grep -A 1 'reddit_posts:' "$CURRENT" | grep 'enabled:' | awk '{print $2}')"
    else
        echo "[ERROR] No config file found at $CURRENT"
        exit 1
    fi
}

case "${1:-}" in
    testing)
        echo "[SWITCH] Switching to TESTING config..."
        if [ ! -f "$TESTING" ]; then
            echo "[ERROR] Testing config not found at $TESTING"
            exit 1
        fi
        cp "$CURRENT" "$CURRENT.backup"
        cp "$TESTING" "$CURRENT"
        echo "[OK] Switched to testing config"
        echo "   - Google Trends: DISABLED"
        echo "   - GitHub Trending: DISABLED"
        echo "   - Safe to run every 5-10 minutes"
        echo ""
        echo "[BACKUP] Backup saved to: $CURRENT.backup"
        ;;
    
    production|prod)
        echo "[SWITCH] Switching to PRODUCTION config..."
        if [ ! -f "$PRODUCTION" ]; then
            echo "[ERROR] Production config not found at $PRODUCTION"
            exit 1
        fi
        cp "$CURRENT" "$CURRENT.backup"
        cp "$PRODUCTION" "$CURRENT"
        echo "[OK] Switched to production config"
        echo "   - Google Trends: ENABLED"
        echo "   - GitHub Trending: ENABLED"
        echo "   - Run once per hour or less"
        echo ""
        echo "[BACKUP] Backup saved to: $CURRENT.backup"
        ;;
    
    status)
        show_status
        ;;
    
    *)
        show_usage
        exit 1
        ;;
esac


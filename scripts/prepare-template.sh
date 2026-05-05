#!/bin/bash

# Script to prepare a clean template version of CareerOS
# This creates sanitized versions of files with personal data

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🔍 Preparing CareerOS template version..."
echo "Repository root: $REPO_ROOT"

# Create a backup branch
echo ""
echo "📦 Creating backup branch..."
cd "$REPO_ROOT"
git checkout -b template-cleanup 2>/dev/null || git checkout template-cleanup

# Sanitize Work_Search_Log.md
echo ""
echo "🧹 Sanitizing Work_Search_Log.md..."
WORK_LOG="$REPO_ROOT/Career/11_Job_Search_Activities/Work_Search_Log.md"
if [ -f "$WORK_LOG" ]; then
    # Create a template version
    sed -i.bak \
        -e 's/- \*\*Name:\*\* Ben Thomas/- **Name:** [Your Name]/' \
        -e 's/- \*\*State:\*\* Texas/- **State:** [Your State]/' \
        -e 's/- \*\*Benefit Year:\*\* 2026/- **Benefit Year:** [Year]/' \
        -e 's/- \*\*Log Start Date:\*\* 2026-01-13/- **Log Start Date:** [YYYY-MM-DD]/' \
        "$WORK_LOG"
    rm -f "$WORK_LOG.bak"
    echo "✅ Sanitized Work_Search_Log.md"
else
    echo "⚠️  Work_Search_Log.md not found"
fi

# Sanitize activity-log.md
echo ""
echo "🧹 Sanitizing activity-log.md..."
ACTIVITY_LOG="$REPO_ROOT/Career/00_Core_OS/activity-log.md"
if [ -f "$ACTIVITY_LOG" ]; then
    # Remove actual log entries, keep only template structure
    # This is a simple approach - you may want to manually review
    echo "⚠️  Please manually review activity-log.md for personal entries"
else
    echo "⚠️  activity-log.md not found"
fi

# Check for other files that might contain personal data
echo ""
echo "🔍 Checking for other files with potential personal data..."
echo ""
echo "Files to review manually:"
echo "  - Any files in Career/01_Resume_and_Profiles/Resume_Master/ (except README.md)"
echo "  - Any files in Career/02_Work_Experience/Roles/ (except README.md)"
echo "  - Any files in Career/07_Applications_and_Interviews/Applications/ (except templates)"
echo "  - Any files in Career/08_Networking_and_References/Contacts/"
echo "  - Any files in Career/11_Job_Search_Activities/Evidence/"

echo ""
echo "✅ Template preparation complete!"
echo ""
echo "Next steps:"
echo "  1. Review the changes: git diff"
echo "  2. Commit the sanitized version: git add . && git commit -m 'Sanitize personal data for template'"
echo "  3. Create the public repo on GitHub"
echo "  4. Push: git remote add template <public-repo-url> && git push template template-cleanup:main"
echo "  5. Make the public repo a template repository in GitHub settings"

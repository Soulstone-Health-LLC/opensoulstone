#!/bin/bash

# Soulstone Quick Health Check
# Run this script to verify your setup is working properly

echo "=========================================="
echo "  Soulstone Quick Health Check"
echo "=========================================="
echo

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

ERRORS=0

echo "1. Checking repository structure..."

# Check for essential files
essential_files=(
    "README.md"
    "LICENSE"
    "CONTRIBUTING.md"
    ".env.example"
    "docker-compose.yaml"
    "docker-compose.dev.yaml"
    "Makefile"
    "validate-setup.sh"
    "init-db.sh"
)

for file in "${essential_files[@]}"; do
    if [[ -f "$file" ]]; then
        print_success "$file exists"
    else
        print_error "$file is missing"
        ERRORS=$((ERRORS + 1))
    fi
done

echo
echo "2. Checking for hardcoded personal information..."

# Check for potential personal info leaks
if grep -r "rodney\|gauna" --include="*.py" --include="*.html" --include="*.js" --include="*.md" --include="*.txt" --include="*.yaml" --include="*.yml" . 2>/dev/null | grep -v "github.com/rodneygauna" | grep -v ".git/" | head -5; then
    print_warning "Found potential personal information references (check above)"
else
    print_success "No obvious personal information found"
fi

echo
echo "3. Checking scripts permissions..."

scripts=("validate-setup.sh" "init-db.sh" "check-environment.sh")
for script in "${scripts[@]}"; do
    if [[ -f "$script" ]]; then
        if [[ -x "$script" ]]; then
            print_success "$script is executable"
        else
            print_error "$script is not executable"
            echo "  Fix with: chmod +x $script"
            ERRORS=$((ERRORS + 1))
        fi
    fi
done

echo
echo "4. Checking Docker configuration..."

if [[ -f "docker-compose.yaml" ]] && [[ -f "docker-compose.dev.yaml" ]]; then
    print_success "Both production and development Docker configs exist"
else
    print_error "Missing Docker configuration files"
    ERRORS=$((ERRORS + 1))
fi

echo
echo "5. Checking environment configuration..."

if [[ -f ".env.example" ]]; then
    if grep -q "your-unique-secret-key" .env.example; then
        print_success "Environment template has placeholder values"
    else
        print_warning "Environment template might have real values"
    fi
else
    print_error ".env.example is missing"
    ERRORS=$((ERRORS + 1))
fi

if [[ -f ".env" ]]; then
    print_warning ".env file exists - ensure it's not committed to git"
else
    print_success "No .env file found (good for repository)"
fi

echo
echo "6. Checking documentation quality..."

if [[ -f "README.md" ]]; then
    if grep -q "Quick Start" README.md && grep -q "Prerequisites" README.md; then
        print_success "README has essential sections"
    else
        print_warning "README might be missing essential sections"
    fi
fi

if [[ -f "CONTRIBUTING.md" ]]; then
    print_success "Contributing guidelines exist"
else
    print_error "CONTRIBUTING.md is missing"
    ERRORS=$((ERRORS + 1))
fi

echo
echo "7. Checking license..."

if [[ -f "LICENSE" ]]; then
    if grep -q "GNU AFFERO GENERAL PUBLIC LICENSE" LICENSE; then
        print_success "AGPL license is properly configured"
    else
        print_warning "License file exists but might not be AGPL"
    fi
else
    print_error "LICENSE file is missing"
    ERRORS=$((ERRORS + 1))
fi

echo
echo "8. Checking GitHub integration..."

if [[ -d ".github/ISSUE_TEMPLATE" ]]; then
    template_count=$(find .github/ISSUE_TEMPLATE -name "*.md" | wc -l)
    if [[ $template_count -gt 0 ]]; then
        print_success "GitHub issue templates exist ($template_count found)"
    else
        print_warning "GitHub issue template directory exists but no templates found"
    fi
else
    print_warning "No GitHub issue templates found"
fi

echo
echo "=========================================="
echo "            Health Check Summary"
echo "=========================================="

if [[ $ERRORS -eq 0 ]]; then
    print_success "Repository appears ready for open source! 🎉"
    echo
    print_info "Next steps:"
    echo "  1. Review all files for any remaining personal information"
    echo "  2. Test the setup process: make validate && make dev-up"
    echo "  3. Consider adding more documentation or examples"
    echo "  4. Set up GitHub repository settings (description, topics, etc.)"
    echo
else
    print_error "Found $ERRORS issue(s) that should be addressed"
    echo
    print_info "Fix the errors above before making the repository public"
fi

echo
print_info "Run './validate-setup.sh' for detailed setup validation"
print_info "Run './check-environment.sh' to check runtime environment"

echo

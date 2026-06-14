#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
README="$REPO_ROOT/README.md"
SKILLS_DIR="$REPO_ROOT/skills"
ERRORS=0

err() { echo "ERROR: $1" >&2; ERRORS=$((ERRORS + 1)); }

extract_frontmatter_field() {
  local file="$1" field="$2"
  awk '/^---/{f++; next} f==1' "$file" | grep "^${field}:" | sed "s/^${field}:[[:space:]]*//"
}

validate_and_collect() {
  local entries=""
  while IFS= read -r skill_md; do
    local skill_dir
    skill_dir="$(dirname "$skill_md")"
    local rel="${skill_md#"$REPO_ROOT/"}"

    local name description references
    name="$(extract_frontmatter_field "$skill_md" name)"
    description="$(extract_frontmatter_field "$skill_md" description)"
    references="$(extract_frontmatter_field "$skill_md" references)"

    [[ -z "$name" ]]        && err "$rel: missing 'name' in frontmatter"
    [[ -z "$description" ]] && err "$rel: missing 'description' in frontmatter"

    if [[ -n "$references" ]]; then
      # parse [file1, file2] or [file1]
      local ref_list
      ref_list="$(echo "$references" | tr -d '[]' | tr ',' '\n' | tr -d ' ')"
      while IFS= read -r ref; do
        [[ -z "$ref" ]] && continue
        local ref_path="$skill_dir/$ref"
        [[ ! -f "$ref_path" ]] && err "$rel: references '$ref' not found at $ref_path"
      done <<< "$ref_list"
    fi

    local skill_path="${skill_dir#"$REPO_ROOT/"}"
    entries="${entries}- **[${name}](${skill_path}/SKILL.md)** — ${description}\n"
  done < <(find "$SKILLS_DIR" -name "SKILL.md" | sort)

  echo -e "$entries"
}

generate_readme() {
  local entries="$1"
  local tmp
  tmp="$(mktemp)"
  awk -v block="$entries" '
    /^<!-- skills-start -->$/ { print; printf "%s\n", block; skip=1; next }
    /^<!-- skills-end -->$/   { skip=0 }
    !skip                     { print }
  ' "$README" > "$tmp"
  mv "$tmp" "$README"
}

entries="$(validate_and_collect)"
generate_readme "$entries"

if [[ "$ERRORS" -gt 0 ]]; then
  echo "$ERRORS error(s) found." >&2
  exit 1
fi

echo "Skills valid. README updated."

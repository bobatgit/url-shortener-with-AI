#!/bin/bash
set -e

# Check if version is provided
if [ -z "$1" ]; then
    echo "Please provide version number (e.g. 1.0.0)"
    exit 1
fi

VERSION=$1

# Validate version format
if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Invalid version format. Please use semantic versioning (e.g. 1.0.0)"
    exit 1
fi

echo "Creating release v$VERSION..."

# Run tests
echo "Running tests..."
pytest

# Create git tag
echo "Creating git tag..."
git tag -a "v$VERSION" -m "Release version $VERSION"

# Push tag
echo "Pushing tag to remote..."
git push origin "v$VERSION"

echo "Release v$VERSION created and pushed!"
echo "GitHub Actions will now build and deploy the release."
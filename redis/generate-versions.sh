#!/bin/bash
set -Eeuo pipefail

cd upstream.git

versions=( */ )
versions=( "${versions[@]%/}" )

packagesUrl='https://raw.githubusercontent.com/redis/redis-hashes/master/README'
packages="$(echo "$packagesUrl" | sed -r 's/[^a-zA-Z.-]+/-/g')"
trap "$(printf 'rm -f %q' "$packages")" EXIT
curl -fsSL "$packagesUrl" -o "$packages"

for version in "${versions[@]}"; do
	rcVersion="${version%-rc}"

	line="$(
		awk '
			{ gsub(/^redis-|[.]tar[.]gz$/, "", $2) }
			$1 == "hash" && $2 ~ /^'"$rcVersion"'([.]|$)/ { print }
		' "$packages" \
			| sort -rV \
			| head -1
	)"

	if [ -n "$line" ]; then
		fullVersion="$(cut -d' ' -f2 <<<"$line")"
		downloadUrl="$(cut -d' ' -f5 <<<"$line")"
		shaHash="$(cut -d' ' -f4 <<<"$line")"
		shaType="$(cut -d' ' -f3 <<<"$line")"
	elif [ "$version" != "$rcVersion" ] && fullVersion="$(
			git ls-remote --tags https://github.com/redis/redis.git "refs/tags/$rcVersion*" \
				| cut -d/ -f3 \
				| cut -d^ -f1 \
				| sort -urV \
				| head -1
	)" && [ -n "$fullVersion" ]; then
		downloadUrl="https://github.com/redis/redis/archive/$fullVersion.tar.gz"
		shaType='sha256'
		shaHash="$(curl -fsSL "$downloadUrl" | "${shaType}sum" | cut -d' ' -f1)"
	else
		echo >&2 "error: full version for $version cannot be determined"
		exit 1
	fi
	[ "$shaType" = 'sha256' ] || [ "$shaType" = 'sha1' ]

	for variant in \
		alpine 32bit '' \
	; do
    dir="$version${variant:+/$variant}"
		[ -d "$dir" ] || continue
    echo "redis_version(\"$fullVersion\", \"$variant\", \"$downloadUrl\", \"$shaType\", \"$shaHash\")."
	done
done

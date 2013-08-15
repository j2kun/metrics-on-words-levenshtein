# the levenshtein metric: comparing edit distance

def memoize(f):
	cache = {}

	def memoizedFunction(*args):
		if args not in cache:
			cache[args] = f(*args)
		return cache[args]

	memoizedFunction.cache = cache
	return memoizedFunction

@memoize
def dist(word1, word2):
	if not word1 or not word2:
		return max(len(word1), len(word2))
	elif word1[-1] == word2[-1]:
		return dist(word1[:-1], word2[:-1])
	else:
		return min(dist(word1[:-1], word2) + 1,
						dist(word1, word2[:-1]) + 1,
						dist(word1[:-1], word2[:-1]) + 1)

levenshteinDist = dist

@memoize
def dist2(word1, word2):
	if not word1 or not word2:
		return max(len(word1), len(word2))
	elif word1[-1] == word2[-1]:
		return dist2(word1[:-1], word2[:-1])
	else:
		minDist = min(dist2(word1[:-1], word2) + 1,
							dist2(word1, word2[:-1]) + 1,
							dist2(word1[:-1], word2[:-1]) + 1)

		# transpositions
		if len(word1) > 1 and len(word2) > 1:
			if word1[-2] == word2[-1]:
				transposedWord1 = word1[:-2] + word1[-1] + word1[-2]
				minDist = min(minDist, dist2(transposedWord1[:-1], word2))

			if word2[-2] == word1[-1]:
				transposedWord2 = word2[:-2] + word2[-1] + word2[-2]
				minDist = min(minDist, dist2(word1, transposedWord2[:-1]))

		return minDist

damerauLevenshteinDist = dist2

def test(f, expected, *args):
	val = f(*args)
	if val != expected:
		print("test failed! args: %s, %s." % args)

test(damerauLevenshteinDist, 2, "ta", "act")
test(damerauLevenshteinDist, 1, "their", "thier")
test(damerauLevenshteinDist, 2, "their", "there")
test(damerauLevenshteinDist, 3, "missconseptoin", "misconception")
test(damerauLevenshteinDist, 25, "abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba")
test(levenshteinDist, 26, "abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba")
test(levenshteinDist, 26, "", "zyxwvutsrqponmlkjihgfedcba")

# CheatCodes - turning BitTorrent links into spoken English

This is a little POC for turning bitstrings into sequences of human-readable,
pronounceable, and potentially memorable words. It's inspired by a cute
technique I first saw in
<a href="http://en.wikipedia.org/wiki/PGPfone">PGPfone</a> in the 1990s.

Given a message of `nbits` and a desired output `word_count`, select a
vocabulary so that `word_count * log2(len(vocab)) >= nbits`.

Split the message by repeatedly dividing it by the length of the vocabulary and
using the modulo as an index into the sorted vocabulary. Repeat until there are
no bits left.

For a 160-bit message (e.g. a SHA-1 BitTorrent hash) and 11 output words, this
requires a vocabulary of 23,913 words, which is just 64kb of static data when
sorted and gzip compressed.

Given an input like:

    # Magnet hash for Iron.Man.3.2013.READNFO.LiNE.XViD-UNiQUE
    a691631dffa7aa1f9ee3cb094b3d5559bfede33d

Produce an output like:

    napa calculating vatican aviator ridiculous georgia
    loosing ingenious teased stout philippines

Now the hash is in a form that could be spoken easily over a telephone, to be
typed into an Android mini PC by your grandmother.

By reversing the process we recover the SHA-1 hash, which is all required to
fetch the movie using BitTorrent DHT (distributed hash table). No central
database or organization was ever involved in the transaction.


## Generating the vocabulary

A naive approach would randomly select words from a known dictionary like
WordNet or `/usr/share/dict/words`, however we can do better.

This POC selects words from a frequency list generated from opensubtitles.org -
common words in this data are likely easy to pronounce, and commonly
recognizable even to an international audience.

The frequency list is further filtered to remove:

* Words with no vowels, and therefore unpronouncable.
* Words containing the letter 'z', helps to avoid spelling issues.
* Words of less than length 3, again to ease recognition over e.g. a telephone.
* Words not appearing in OS X `/usr/share/dict/words`. This removes a lot of
  swearing and made up terms.
* Case sensitivity is ignored.

There is a tradeoff between vocabulary size and the number of output words:
fewer output words increases vocabulary size, which likely decreases
recognizability and memorability.

The frequency list comes from <a
href="http://invokeit.wordpress.com/frequency-word-lists/">Invoke IT weblog</a>.


## Improvements

* Humans are bad at spelling and typing, so the potential for input errors is
  high. Addition of parity bits or an error-correcting code would improve
  useability, for example by presenting an immediate error to the user, or
  correcting a limited range of mistakes.

  Ideally parity would be interleaved instead of concatenated, improving a
  GUI's responsiveness by alerting the moment the first incorrect word is
  entered.

* Since we're working from a small vocabulary, correct spellings could be
  suggested.

* Ideally the scheme would be future-proofed using some *selector bits* too.
  For example, addition of 3 bits to the message would allow disambiguating a
  BitTorrent link from a FreeNet link, with enough space left to add 6 new link
  types in the future.

* Alternatively, selectors and versioning could be implemented by restricting
  the first word to a very small vocabulary. By never reusing that vocabulary
  for the first word in a later version, a client can disambiguate the scheme
  in use.


## Please build this

Imagine a perfectly legal app in the Google Play store that was a BitTorrent
client powered by CheatCodes. The client would fetch via DHT, and depending on
the file content:

* If it's media, download and play the file.
* If it's a playlist, fetch the contents and perhaps enqueue for download.
* If it's a directory, render the contents visually to the user.

Now imagine including a public key, a schedule, a publisher and a list of
continuation URLs. The client polls the continuation URLs daily looking for a
message matching the key. Once found, the client downloads the hash from the
message, repeating the process daily to form an independent sequence of
publications with potentially no fixed, central source.

Suppose the continuation message is simply a list of words from the
vocabularity appearing anywhere in the HTML, interspersed with arbitrary extra
words or formatting. `word_count` is extended to include the length of the
public key signature.

Now imagine any random low-volume forum, newsgroup, comments section,
Mailinator mailbox, or even Twitter hashtag used as a continuation URL.

Preventing publication of the continuation message requires banning publication
of any sequence of the 23,913 most common English words, interspersed with
arbitrary extra words or formatting. Even with knowledge of the public key,
preventing publication on e.g. Twitter or a weblog comments section would
require scanning for messages embedded across item boundaries.

Given just 11 words spoken over a telephone, everyone has a totally
decentralized, censorship-resistant method to publish their own television
channel to anyone with an Android device plugged into their TV.

A *directory of channels* might work simiarly, where anyone observing some
channels can publish their history and hashes for the most recent publication.
This would allow 11 words to represent a curated list, e.g. a person's
favourite SciFi TV shows.



Note: see http://tools.ietf.org/html/rfc1751 for another implementation

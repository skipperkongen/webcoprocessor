# Good tasks for web co-processors

* Compute intensive rather than data intensive (small pipe between query engine and core = move code rather than big data)
* Verifiable results, should be fast compared to computing results. Alternatively just trust the results and see how it goes (Wikipedia model).
* Web cores access big data directly on the internet, e.g. CDN (making data addressable on CDN is separate challenge, for geodata think linearization, e.g. hilbert-curve)
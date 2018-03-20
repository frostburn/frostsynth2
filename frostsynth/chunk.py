from numpy import concatenate, zeros


def chunkify(data, window, overlap, ljust=False):
    size = len(window)
    delta = size // overlap
    chunks = []
    if ljust:
        data = concatenate((zeros(delta), data))
    if len(data) % size != 0:
        data = concatenate((data, zeros(size - len(data) % size)))
    while len(data) >= size:
        chunks.append(data[:size] * window)
        data = data[delta:]
    return chunks


def dechunkify(chunks, overlap):
    size = len(chunks[0])
    delta = size // overlap
    components = []
    for i in range(overlap):
        parts = chunks[i::overlap]
        if parts:
            component = concatenate(parts)
        else:
            component = zeros(0)
        component = concatenate((zeros(delta * i), component))
        components.append(component)
    max_len = max(map(len, components))
    data = 0
    for component in components:
        component = concatenate((component, zeros(max_len - len(component))))
        data += component
    return data / float(overlap)

from numpy import concatenate, zeros


def chunkify(data, window, overlap):
    size = len(window)
    delta = size // overlap
    chunks = []
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
        component = concatenate(chunks[i::overlap])
        component = concatenate((zeros(delta * i), component))
        components.append(component)
    max_len = max(map(len, components))
    data = 0
    for component in components:
        component = concatenate((component, zeros(max_len - len(component))))
        data += component
    return data / float(overlap)

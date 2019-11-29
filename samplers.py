import random

import torch.utils


class RandomIdentityBatchSampler(torch.utils.data.Sampler):
    def __init__(self, data, batch_size, num_identities=4):
        super().__init__(data)

        self.data = data
        self.batch_size = batch_size
        self.num_identities = num_identities

    def __len__(self):
        return len(self.data) // self.batch_size

    def __iter__(self):
        id_to_indices = [[] for _ in range(self.data.max() + 1)]
        for index, id in self.data.iteritems():
            id_to_indices[id].append(index)

        for indices in id_to_indices:
            random.shuffle(indices)
        random.shuffle(id_to_indices)

        batches = []
        batch = []
        while len(id_to_indices) > 0:
            for indices in id_to_indices:
                num_identities = min(self.num_identities, len(indices))
                for _ in range(num_identities):
                    batch.append(indices.pop())

                    if len(batch) == self.batch_size:
                        batches.append(batch)
                        batch = []

            id_to_indices = [indices for indices in id_to_indices if len(indices) > 0]

        assert len(batches) == len(self)
        random.shuffle(batches)

        return iter(batches)

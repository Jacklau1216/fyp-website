from GLTR import server


class GPT2():
    def __init__(self):
        self.model = server.projects["gpt-2-small"]

    def analyze(self, text ,topk=40):
        return self.model.lm.check_probabilities(text, topk=topk)
        # payload = {'bpe_strings': bpe_strings,
        # 'real_topk': real_topk,
        # 'pred_topk': pred_topk}

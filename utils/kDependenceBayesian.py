import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.metrics import mutual_info_score

class KDBClassifier:

    def __init__(self, k=2, alpha=1):
        self.k = k
        self.alpha = alpha

    def _conditional_mutual_information(self, x, y, c):
        """
        Calcula I(X;Y|C)
        """
        c_values = np.unique(c)

        total = 0

        for cv in c_values:
            mask = c == cv

            if mask.sum() == 0:
                continue

            px = mask.sum() / len(c)

            total += px * mutual_info_score(
                x[mask],
                y[mask]
            )

        return total

    def fit(self, X, y):

        X = pd.DataFrame(X).copy()

        self.features_ = list(X.columns)

        # --------------------------
        # 1. Informação mútua
        # --------------------------
        mi = {}

        for col in self.features_:
            mi[col] = mutual_info_score(X[col], y)

        ordered = sorted(
            self.features_,
            key=lambda c: mi[c],
            reverse=True
        )

        self.order_ = ordered

        # --------------------------
        # 2. Escolha dos pais
        # --------------------------
        self.parents_ = {}

        for i, feature in enumerate(ordered):

            previous = ordered[:i]

            if len(previous) == 0:
                self.parents_[feature] = []
                continue

            scores = []

            for parent in previous:

                cmi = self._conditional_mutual_information(
                    X[feature].values,
                    X[parent].values,
                    y
                )

                scores.append((parent, cmi))

            scores.sort(
                key=lambda x: x[1],
                reverse=True
            )

            self.parents_[feature] = [
                p for p, _ in scores[:self.k]
            ]

        # --------------------------
        # 3. Probabilidades da classe
        # --------------------------
        self.class_counts_ = y.value_counts().to_dict()

        self.classes_ = sorted(y.unique())

        # valores possíveis das notas
        self.feature_values_ = {
            col: sorted(X[col].unique())
            for col in self.features_
        }

        # --------------------------
        # 4. Tabelas de probabilidade
        # --------------------------
        self.tables_ = {}

        for feature in self.features_:

            parents = self.parents_[feature]

            table = defaultdict(int)

            for idx in range(len(X)):

                row = X.iloc[idx]

                key = (
                    y.iloc[idx],
                    row[feature],
                    tuple(row[p] for p in parents)
                )

                table[key] += 1

            self.tables_[feature] = table

        self.n_samples_ = len(X)

        return self

    def _feature_probability(
        self,
        feature,
        value,
        parent_values,
        cls
    ):

        table = self.tables_[feature]

        key = (
            cls,
            value,
            parent_values
        )

        numerator = table[key]

        denominator = 0

        for v in self.feature_values_[feature]:

            denominator += table[
                (cls, v, parent_values)
            ]

        num_values = len(self.feature_values_[feature])

        return (
            numerator + self.alpha
        ) / (
            denominator + self.alpha * num_values
        )

    def predict_proba(self, X):

        X = pd.DataFrame(X)

        probs = []

        for _, row in X.iterrows():

            class_probs = {}

            for cls in self.classes_:

                # Prior P(C)
                prior = (
                    self.class_counts_[cls] + self.alpha
                ) / (
                    self.n_samples_
                    + self.alpha * len(self.classes_)
                )

                prob = np.log(prior)

                for feature in self.features_:

                    parents = self.parents_[feature]

                    parent_values = tuple(
                        row[p]
                        for p in parents
                    )

                    p = self._feature_probability(
                        feature,
                        row[feature],
                        parent_values,
                        cls
                    )

                    prob += np.log(p)

                class_probs[cls] = prob

            max_log = max(class_probs.values())

            exp_probs = {
                c: np.exp(v - max_log)
                for c, v in class_probs.items()
            }

            total = sum(exp_probs.values())

            probs.append({
                c: exp_probs[c] / total
                for c in self.classes_
            })

        return pd.DataFrame(probs)

    def predict(self, X):

        probs = self.predict_proba(X)

        return probs.idxmax(axis=1).tolist()
    
    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, state):

        obj = cls()
        obj.__dict__.update(state)

        return obj
    
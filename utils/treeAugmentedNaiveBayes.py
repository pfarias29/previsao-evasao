import pandas as pd
import numpy as np
import networkx as nx

from collections import defaultdict
from sklearn.metrics import mutual_info_score


class TANClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha

    def _conditional_mutual_information(
        self,
        x,
        y,
        c
    ):
        """
        I(X;Y|C)
        """

        total = 0

        for cls in np.unique(c):

            mask = c == cls

            if mask.sum() == 0:
                continue

            weight = mask.sum() / len(c)

            total += weight * mutual_info_score(
                x[mask],
                y[mask]
            )

        return total

    def fit(self, X, y):

        X = pd.DataFrame(X).copy()

        self.features_ = list(X.columns)

        self.classes_ = sorted(y.unique())

        self.n_samples_ = len(X)

        # -----------------------
        # Prior da classe
        # -----------------------

        self.class_counts_ = (
            y.value_counts()
            .to_dict()
        )

        # -----------------------
        # Valores possíveis
        # -----------------------

        self.feature_values_ = {}

        for col in self.features_:

            vals = sorted(
                set(X[col].unique())
                | {-1,0,1,2,3,4,5}
            )

            self.feature_values_[col] = vals

        # -----------------------
        # Grafo completo
        # -----------------------

        G = nx.Graph()

        for feature in self.features_:
            G.add_node(feature)

        for i in range(len(self.features_)):

            for j in range(i + 1, len(self.features_)):

                f1 = self.features_[i]
                f2 = self.features_[j]

                weight = (
                    self._conditional_mutual_information(
                        X[f1].values,
                        X[f2].values,
                        y.values
                    )
                )

                G.add_edge(
                    f1,
                    f2,
                    weight=weight
                )

        # -----------------------
        # Maximum Spanning Tree
        # -----------------------

        mst = nx.maximum_spanning_tree(G)

        root = self.features_[0]

        self.parents_ = {
            root: []
        }

        visited = set([root])

        queue = [root]

        while queue:

            current = queue.pop(0)

            for neighbor in mst.neighbors(current):

                if neighbor not in visited:

                    visited.add(neighbor)

                    self.parents_[neighbor] = [
                        current
                    ]

                    queue.append(neighbor)

        # -----------------------
        # Tabelas
        # -----------------------

        self.tables_ = {}

        for feature in self.features_:

            parents = self.parents_.get(
                feature,
                []
            )

            table = defaultdict(int)

            for idx in range(len(X)):

                row = X.iloc[idx]

                key = (
                    y.iloc[idx],
                    row[feature],
                    tuple(
                        row[p]
                        for p in parents
                    )
                )

                table[key] += 1

            self.tables_[feature] = table

        return self

    def _feature_probability(
        self,
        feature,
        value,
        parent_values,
        cls
    ):

        table = self.tables_[feature]

        numerator = table[
            (
                cls,
                value,
                parent_values
            )
        ]

        denominator = 0

        for v in self.feature_values_[feature]:

            denominator += table[
                (
                    cls,
                    v,
                    parent_values
                )
            ]

        return (
            numerator + self.alpha
        ) / (
            denominator
            + self.alpha
            * len(
                self.feature_values_[feature]
            )
        )

    def predict_proba(self, X):

        X = pd.DataFrame(X)

        results = []

        for _, row in X.iterrows():

            class_probs = {}

            for cls in self.classes_:

                prior = (
                    self.class_counts_[cls]
                    + self.alpha
                ) / (
                    self.n_samples_
                    + self.alpha
                    * len(self.classes_)
                )

                log_prob = np.log(prior)

                for feature in self.features_:

                    parents = self.parents_.get(
                        feature,
                        []
                    )

                    parent_values = tuple(
                        row[p]
                        for p in parents
                    )

                    p = (
                        self._feature_probability(
                            feature,
                            row[feature],
                            parent_values,
                            cls
                        )
                    )

                    log_prob += np.log(p)

                class_probs[cls] = log_prob

            max_log = max(
                class_probs.values()
            )

            exp_probs = {
                c: np.exp(v - max_log)
                for c, v in class_probs.items()
            }

            total = sum(
                exp_probs.values()
            )

            results.append({
                c: exp_probs[c] / total
                for c in self.classes_
            })

        return pd.DataFrame(results)

    def predict(self, X):

        probs = self.predict_proba(X)

        return (
            probs.idxmax(axis=1)
            .astype(int)
            .tolist()
        )
    
    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, state):

        obj = cls()
        obj.__dict__.update(state)

        return obj
    
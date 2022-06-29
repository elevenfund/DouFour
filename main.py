# %%
from email import header
import random
import copy
import pandas as pd

from pendulum import instance


class Card:
    def __init__(self) -> None:
        card_normal = ["3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A", "2"]
        king = ["M", "N"]
        self.all_cards = [*card_normal * 8, *king * 2]

        self.pp1 = []
        self.pp2 = []
        self.pp3 = []
        self.pp4 = []

    def hand_cards(self, player=None):
        if not player:
            player = self.player
        elif player == 1:
            player = self.p1
        elif player == 2:
            player = self.p2
        elif player == 3:
            player = self.p3
        elif player == 4:
            player = self.p4
        print(self.pretty_cards_list(player))
        print("-"*60)
        print(self.pretty_cards_compose(player))

    @staticmethod
    def pretty_cards_compose(cards):

        cards = sorted(cards, key=Card.transfer_card_int)
        count = {}
        for key in cards:
            count[key] = count.get(key, 0) + 1
        # double
        ss = []
        dd = []
        tt = []
        ff = []

        pretty = ""
        for key in count:
            if count[key] == 1:
                ss.append(key)
            elif count[key] == 2:
                dd.append(key*2)
            elif count[key] == 3:
                tt.append(key*3)
            elif count[key] >= 4:
                ff.append(key*count[key])
        for k in [ss, dd, tt, ff]:
            if len(k) > 0:
                pretty += "|".join(k)
                pretty += "\n"
        return pretty

    @staticmethod
    def pretty_cards_list(cards):
        cards = sorted(cards, key=Card.transfer_card_int)
        cards = [str(c) for c in cards]
        str_cards = "|".join(cards)
        return str_cards

    @staticmethod
    def pandas_sort(series):
        return pd.Series(series).apply(Card.transfer_card_int)

    @staticmethod
    def transfer_card_int(s):
        if s == "A":
            s = 21
        elif s == "2":
            s = 22
        elif s == "T":
            s = 10
        elif s == "J":
            s = 11
        elif s == "Q":
            s = 12
        elif s == "K":
            s = 13
        elif s == "N":
            s = 31
        elif s == "M":
            s = 32
        return int(s)

    # @property
    # def all_cards(self):
    #     return self.all_cards()
    # def show_table(self):
    #     self.hands_cards = pd.value_counts(self.all_cards)
    #     return result

    @staticmethod
    def is_3_p_2(s):
        if len(s) == 5:
            return

    def disclosure_cards(self):
        for i in range(4):
            cards = eval(f"self.p{i+1}")
            print(f"Players {i+1}: {self.pretty_cards_list(cards)}")

    def public_cards(self):
        for i in [1, 2, 3, 4, "_unknown"]:
            cards = eval(f"self.pp{i}")
            print(f"Players {i}: {self.pretty_cards_list(cards)}")

    def public_cards_df(self):
        pp1_df = pd.DataFrame(pd.value_counts(self.pp1), columns=["p1"])
        pp2_df = pd.DataFrame(pd.value_counts(self.pp2), columns=["p2"])
        pp3_df = pd.DataFrame(pd.value_counts(self.pp3), columns=["p3"])
        pp4_df = pd.DataFrame(pd.value_counts(self.pp3), columns=["p4"])
        unknown_df = pd.DataFrame(pd.value_counts(self.pp_unknown), columns=["unknown"])
        df = pp1_df.join(pp2_df, how="outer").join(pp3_df, how="outer").join(
            pp4_df, how="outer").join(unknown_df, how="outer").fillna(0).astype(int)
        return df.sort_index(key=self.pandas_sort, axis=0)

    def shuffle_cards(self):
        random_cards = copy.deepcopy(self.all_cards)
        print(len(random_cards))
        random.shuffle(random_cards)
        normal_cards = [random_cards[i:i+25] for i in [0, 25, 50, 75]]
        self.extra_cards = random_cards[-8:]
        self.p1 = normal_cards[0]
        self.p2 = normal_cards[1]
        self.p3 = normal_cards[2]
        self.p4 = normal_cards[3]
        for i in range(4):
            print(f"Cards {i+1}: {self.pretty_cards_list(normal_cards[i])}")

    def set_farmer(self, n):
        if n == 1:
            pass
        elif n == 2:
            self.p1, self.p2 = self.p2, self.p1
        elif n == 3:
            self.p1, self.p3 = self.p3, self.p1
        elif n == 4:
            self.p1, self.p4 = self.p4, self.p1
        self.p1.extend(self.extra_cards)

    def set_player(self, num):
        # all_cards -> farmer cards (pp1) + unknown + pp1 + pp2 +pp3
        self.player = eval(f"self.p{num}")
        self.pp_unknown = copy.deepcopy(self.all_cards)
        for c in self.player:
            self.pp_unknown.remove(c)
        if num == 1:
            self.pp1 = self.player
        if num == 2:
            self.pp2 = self.player
        if num == 3:
            self.pp3 = self.player
        if num == 4:
            self.pp4 = self.player
        if num != 1:
            self.pp1 = self.extra_cards
            for i in self.extra_cards:
                self.pp_unknown.remove(i)

    def run(self, p, cards):
        p = eval(f"self.p{p}")
        if isinstance(cards, str):
            cards = list(cards)
        for c in cards:
            self.all_cards.remove(c)
            p.remove(c)

    #     else:

    def table_cards(self):
        pass


class Player:

    show_card = False

    def __init__(self, name,  cards) -> None:
        self.name = name
        self.cards = cards

    def show_cards(self):

        cards = sorted(self.cards, key=Card.transfer_card_int)
        cards = [str(c) for c in cards]
        str_cards = "|".join(cards)

        print(f"Player {self.name}: {str_cards}")


# %%
# !shuffle_cards
cards = Card()
cards.shuffle_cards()

# %%
# !set famer
cards.set_farmer(1)
cards.disclosure_cards()

# %%
cards.set_player(2)
cards.public_cards()
# %%
cards.public_cards()
cards.disclosure_cards()
# %%
# cards.run(2, "AAA22")
# cards.disclosure_cards()
# %%

cards.public_cards_df()
# %%

cards.hand_cards()
# %%

# %%

# %%

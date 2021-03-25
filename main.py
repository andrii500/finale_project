import re


class Frame:
    def __init__(self):
        self.score = []

    @staticmethod
    def valid_input():
        while True:
            number = input("Enter number of pins that knocked down in this throw: ")
            if number.isdigit():
                number = int(number)
                if number < 0 or number > 10:
                    print("You number must be between 0 and 10")
                else:
                    return number
            else:
                print("You must enter a number")

    def set_score(self):
        while True:
            score_ = self.valid_input()
            if score_ == 10 and self.score == []:
                self.score.append("X(strike)")
                break
            else:
                if not self.score:
                    self.score.append(score_)
                else:
                    if self.score[0]:
                        if (10 - self.score[0]) < score_:
                            print("The number of pins in the second throw cant be this value, please rewrite")
                        else:
                            if self.score[0] + score_ == 10:
                                self.score.append("/(spare)")
                                break
                            else:
                                self.score.append(f"{score_}(open)")
                                break

    def set_score_in_last_frame(self):
        num = 0
        while True:
            if num >= 3:
                break
            else:
                score_ = self.valid_input()
                if score_ == 10 and num == 0:
                    self.score.append("X(strike)")
                    num += 1
                elif score_ == 10 and num == 1:
                    if self.score[0] == "X(strike)":
                        self.score.append("X(strike)")
                        num += 1
                    else:
                        print("The number of pins in the second throw cant be this value, please rewrite")
                elif score_ == 10 and num == 2:
                    if self.score[1] == "X(strike)":
                        self.score.append("X(strike)")
                        num += 1
                    elif self.score[1] == "/(spare)":
                        self.score.append("X(strike)")
                        num += 1
                    else:
                        print("The number of pins in the second throw cant be this value, please rewrite")

                elif score_ < 10 and num == 0:
                    self.score.append(score_)
                    num += 1
                elif score_ < 10 and num == 1:
                    if self.score[0] != "X(strike)":
                        if (10 - self.score[0]) < score_:
                            print("The number of pins in the second throw cant be this value, please rewrite")
                        else:
                            if self.score[0] + score_ == 10:
                                self.score.append("/(spare)")
                                num += 1
                            else:
                                self.score.append(f"{score_}(open)")
                                num += 2
                    elif self.score[0] == "X(strike)":
                        self.score.append(score_)
                        num += 1
                elif score_ < 10 and num == 2:
                    if self.score[1] != "X(strike)" and self.score[1] != "/(spare)":
                        if (10 - self.score[1]) < score_:
                            print("The number of pins in the second throw cant be this value, please rewrite")
                        else:
                            if self.score[1] + score_ == 10:
                                self.score.append("/(spare)")
                                num += 1
                            else:
                                self.score.append(f"{score_}(open)")
                                num += 1
                    elif self.score[1] == "X(strike)":
                        self.score.append(score_)
                        num += 1
                    elif self.score[1] == "/(spare)":
                        self.score.append(score_)
                        num += 1


class Game:
    def __init__(self):
        self.score_table = {}

    def set_players(self):
        while True:
            str_of_players = input("Enter names of players divided by space: ")
            if not str_of_players:
                print("It must be at least one player")
            else:
                for i in range(len(str_of_players.split(" "))):
                    self.score_table[str_of_players.split(" ")[i]] = []
                break

    def set_score_table(self, frame_score, name):
        self.score_table[name].append(frame_score)

    def get_score_table(self):
        str_ = "Name      Frame1             Frame2             Frame3             Frame4             Frame5" \
               "             Frame6             Frame7             Frame8             Frame9             Frame10 \n"
        for i in self.score_table:
            str_ += f"{i}        "
            for j in self.score_table[i]:
                for k in j:
                    str_ += f"{k} "
                str_ += "     "
            str_ += "\n"
        return str_

    def get_result_of_game(self):
        player = ''
        winner_score = 0

        for player_ in self.score_table:
            res = []
            total_score = 0
            for x in self.score_table[player_]:
                res.extend(x if isinstance(x, list) else [x])

            for i in range(len(res)):
                if len(res) > i + 2:
                    if res[i] == "X(strike)" and res[i + 1] == "X(strike)" and res[i + 2] == "X(strike)":
                        total_score += 30
                    elif res[i] == "X(strike)" and res[i + 2] == "/(spare)":
                        total_score += 20
                    elif res[i] == "X(strike)" and (type(res[i + 2]) == str) and ("(open)" in res[i + 2]):
                        total_score += 10
                        total_score += res[i + 1]
                        total_score += int(re.findall("\d", res[i + 2])[0])
                    if res[i] == "X(strike)" and res[i + 1] == "X(strike)" and type(res[i + 2]) == int:
                        total_score += 20
                        total_score += res[i + 2]
                        continue

                if len(res) > i + 1:
                    if res[i] == "/(spare)" and res[i + 1] == "X(strike)":
                        total_score += 10 - res[i - 1]
                        total_score += 10
                    elif res[i] == "/(spare)" and type(res[i + 1]) == int:
                        total_score += 10 - res[i - 1]
                        total_score += res[i + 1]

                if len(res) == i + 1 or len(res) == i:
                    if type(res[i]) == str and ("(open)" in res[i]):
                        total_score += int(re.findall("\d", res[i])[0])

                    elif type(res[i]) == int:
                        total_score += res[i]
                    else:
                        break
                else:
                    if type(res[i]) == str and ("(open)" in res[i]):
                        total_score += int(re.findall("\d", res[i])[0])

                    elif type(res[i]) == int:
                        total_score += res[i]

            if winner_score < total_score:
                player = player_
                winner_score = total_score

        return f"Winner of the game is {player}, with total score - {winner_score}"


def play():
    game = Game()
    game.set_players()

    for i in range(1, 11):
        for name in game.score_table:
            print(f"{name} throw now")
            frame = Frame()
            if i == 10:
                frame.set_score_in_last_frame()
            else:
                frame.set_score()
            game.set_score_table(frame.score, name)

    print(game.get_score_table())
    print(game.get_result_of_game())


play()

from itertools import permutations
from pprint import pprint


class NamedTuple(tuple):
    short_name = 'list'

    def __str__(self):
        return self.short_name

    def __repr__(self):
        return self.__str__()

    def set_short_name(self, new_name):
        self.short_name = new_name


class hn_wrapper(object):
    def __init__(self, it):
        self.it = iter(it)
        self._hasnext = None

    def __iter__(self):
        return self

    def next(self):
        if self._hasnext:
            result = self._thenext
        else:
            result = next(self.it)
        self._hasnext = None
        return result

    def hasnext(self):
        if self._hasnext is None:
            try:
                self._thenext = next(self.it)
            except StopIteration:
                self._hasnext = False
            else:
                self._hasnext = True
        return self._hasnext

COLORS = ('blue', 'green', 'red', 'white', 'yellow')
COLORS = NamedTuple(COLORS)
COLORS.set_short_name('COLORS')

PETS = ('cat', 'bird', 'dog', 'fish', 'horse')
PETS = NamedTuple(PETS)
PETS.set_short_name('PETS')

BEVERAGES = ('beer', 'coffee', 'milk', 'tea', 'water')
BEVERAGES = NamedTuple(BEVERAGES)
BEVERAGES.set_short_name('BEVERAGES')

CIGARETTES = ('Dunhill', 'Rothmans', 'Pall Mall', 'Winfield', 'Marlboro')
CIGARETTES = NamedTuple(CIGARETTES)
CIGARETTES.set_short_name('CIGARETTES')

NATIONALITY = ('Norwegian', 'Brit', 'Dane', 'German', 'Swede')
NATIONALITY = NamedTuple(NATIONALITY)
NATIONALITY.set_short_name('NATIONALITY')

NUMBERS = ('1', '2', '3', '4', '5')
NUMBERS = NamedTuple(NUMBERS)
NUMBERS.set_short_name('NUMBERS')

QUESTIONS = (COLORS, PETS, BEVERAGES, CIGARETTES, NATIONALITY, NUMBERS)
text_questions = ["color", "pet", "beverage", "cigarettes", "nationality", "number"]


def get_dict_by_word(word: str) -> set:
    for kind in QUESTIONS:
        if word in set(kind):
            return kind


def predicates_to_list(predicate: str):
    l = [(el.split('-')) for el in predicate]
    list_of_kinds = list((get_dict_by_word(i), i, get_dict_by_word(j), j) for i, j in l)
    list_of_kinds.sort(key=lambda el: min(QUESTIONS.index(el[0]), QUESTIONS.index(el[2])))
    return list_of_kinds


def get_kind_of_problem(citizens: set, list_of_predicates: list, has_next_flags: dict):
    problem_kind = set()
    for man in citizens:
        for pair in list_of_predicates:
            if (man[pair[0]] == pair[1] and man[pair[2]] != pair[3]) or (man[pair[0]] != pair[1] and man[pair[2]] == pair[3]):
                # print(pair, "not in citizens = ", citizens)
                if pair[0] in has_next_flags:
                    problem_kind.add(pair[0])
                if pair[2] in has_next_flags:
                    problem_kind.add(pair[2])

                problem_kind.add(pair[2])
                problem_kind.add(pair[0])

        # print(problem_kind, {k: v for k, v in has_next_flags.items() if v is False}, pair[0], pair[2])
    print(problem_kind, 'is problem kind')
    return get_minimal_problem_by_weight(problem_kind, has_next_flags)


def get_minimal_problem_by_weight(in_set: set, has_next_flags):
    print(has_next_flags, "||||", in_set)
    for el in has_next_flags:
        if has_next_flags[el] is False and el in in_set:
            in_set.remove(el)
    #         # print('remove' + el)
    #         pass
    # print('in_set = ' + str(in_set))
    # if in_set:
    #     res = min(in_set, key=lambda el: QUESTIONS.index(el))
    # else:
    #     res = None
    #     print("wtf?")
    # return res
    res = min(in_set, key=lambda el: QUESTIONS.index(el))
    # print(res, has_next_flags, sep="    ")
    return res


def get_citizens_by_relations(relations):
    predicates = predicates_to_list(relations)
    break_flag = None
    c_iter = hn_wrapper(iter(permutations(COLORS)))
    has_next = dict()
    while c_iter.hasnext():
        c = c_iter.next()
        has_next[COLORS] = c_iter.hasnext()

        pe_iter = hn_wrapper(iter(permutations(PETS)))
        while pe_iter.hasnext():
            pe = pe_iter.next()
            has_next[PETS] = pe_iter.hasnext()

            b_iter = hn_wrapper(iter(permutations(BEVERAGES)))
            while b_iter.hasnext():
                b = b_iter.next()
                has_next[BEVERAGES] = b_iter.hasnext()

                ci_iter = hn_wrapper(iter(permutations(CIGARETTES)))
                while ci_iter.hasnext():
                    ci = ci_iter.next()
                    has_next[CIGARETTES] = ci_iter.hasnext()

                    nation_iter = hn_wrapper(iter(permutations(NATIONALITY)))
                    while nation_iter.hasnext():
                        n = nation_iter.next()
                        has_next[NATIONALITY] = nation_iter.hasnext()

                        numb_iter = hn_wrapper(iter(permutations(NUMBERS)))
                        while numb_iter.hasnext():
                            numb = numb_iter.next()
                            has_next[NUMBERS] = numb_iter.hasnext()

                            citizens = ({COLORS: c[0], PETS: pe[0], BEVERAGES: b[0],
                                         CIGARETTES: ci[0], NATIONALITY: n[0], NUMBERS: numb[0]},
                                        {COLORS: c[1], PETS: pe[1], BEVERAGES: b[1],
                                         CIGARETTES: ci[1], NATIONALITY: n[1], NUMBERS: numb[1]},
                                        {COLORS: c[2], PETS: pe[2], BEVERAGES: b[2],
                                         CIGARETTES: ci[2], NATIONALITY: n[2], NUMBERS: numb[2]},
                                        {COLORS: c[3], PETS: pe[3], BEVERAGES: b[3],
                                         CIGARETTES: ci[3], NATIONALITY: n[3], NUMBERS: numb[3]},
                                        {COLORS: c[4], PETS: pe[4], BEVERAGES: b[4],
                                         CIGARETTES: ci[4], NATIONALITY: n[4], NUMBERS: numb[4]})
                            break_flag = get_kind_of_problem(citizens, predicates, has_next)
                            if break_flag != NUMBERS:
                                break
                            else:
                                continue
                        if break_flag != NATIONALITY:
                            # print("by nation")
                            break
                        else:
                            continue
                    if break_flag != CIGARETTES:
                        # print("by cigar")
                        break
                    else:
                        continue
                if break_flag != BEVERAGES:
                    # print("by beverage")
                    break
                else:
                    continue
            if break_flag != PETS:
                # print("by pet")
                break
            else:
                continue
        if break_flag != COLORS:
            # print("by color")
            break
        else:
            continue
    if break_flag is None:
        # print('NONE!')
        pass
    print(citizens)
    return citizens


def get_property_by_token(citizens, sign, question):
    dict_kind = get_dict_by_word(sign)
    for man in citizens:
        if man[dict_kind] == sign:
            return man[QUESTIONS[text_questions.index(question)]]


def answer(relations_sring, question_string: str):
    citizens = get_citizens_by_relations(relations_sring)
    sign, question = question_string.split("-")
    return get_property_by_token(citizens, sign, question)


if __name__ == '__main__':
    # citizens = ({PETS: 'cat', CIGARETTES: 'Dunhill', NATIONALITY: 'Norwegian', BEVERAGES: 'beer', COLORS: 'yellow', NUMBERS: '1'}, {PETS: 'bird', CIGARETTES: 'Rothmans', NATIONALITY: 'Brit', BEVERAGES: 'coffee', COLORS: 'white', NUMBERS: '2'}, {PETS: 'dog', CIGARETTES: 'Pall Mall', NATIONALITY: 'Dane', BEVERAGES: 'milk', COLORS: 'red', NUMBERS: '3'}, {PETS: 'fish', CIGARETTES: 'Winfield', NATIONALITY: 'German', BEVERAGES: 'tea', COLORS: 'green', NUMBERS: '4'}, {PETS: 'horse', CIGARETTES: 'Marlboro', NATIONALITY: 'Swede', BEVERAGES: 'water', COLORS: 'blue', NUMBERS: '5'})
    # predicates = ('Marlboro-blue', 'Norwegian-Dunhill', 'Brit-3', 'German-coffee', 'beer-white', 'cat-water',
    #               'horse-2', 'milk-3', '4-Rothmans',
    #               'dog-Swede', 'Norwegian-1', 'horse-Marlboro',
    #               'bird-Brit', '4-green', 'Winfield-beer',
    #               'Dane-blue', '5-dog', 'blue-horse',
    #               'yellow-cat', 'Winfield-Swede', 'tea-Marlboro')
    # pprint(get_kind_of_problem(citizens, predicates_to_list(predicates), dict())
    # )


    pprint(answer(
        ('Marlboro-blue', 'Norwegian-Dunhill', 'Brit-3', 'German-coffee', 'beer-white', 'cat-water',
                   'horse-2', 'milk-3', '4-Rothmans',
                   'dog-Swede', 'Norwegian-1', 'horse-Marlboro',
                   'bird-Brit', '4-green', 'Winfield-beer',
                   'Dane-blue', '5-dog', 'blue-horse',
                   'yellow-cat', 'Winfield-Swede', 'tea-Marlboro'),
                  'fish-color')
    )
    # assert answer(('Norwegian-Dunhill', 'Marlboro-blue', 'Brit-3',
    #                'German-coffee', 'beer-white', 'cat-water',
    #                'horse-2', 'milk-3', '4-Rothmans',
    #                'dog-Swede', 'Norwegian-1', 'horse-Marlboro',
    #                'bird-Brit', '4-green', 'Winfield-beer',
    #                'Dane-blue', '5-dog', 'blue-horse',
    #                'yellow-cat', 'Winfield-Swede', 'tea-Marlboro'),
    #               'fish-color') == 'green'

    # q = ('Marlboro-blue', 'Norwegian-Dunhill', 'Brit-3', 'German-coffee', 'beer-white', 'cat-water',
    #                'horse-2', 'milk-3', '4-Rothmans',
    #                'dog-Swede', 'Norwegian-1', 'horse-Marlboro',
    #                'bird-Brit', '4-green', 'Winfield-beer',
    #                'Dane-blue', '5-dog', 'blue-horse',
    #                'yellow-cat', 'Winfield-Swede', 'tea-Marlboro')
    # print(get_dict_by_word('yellow'))
    # pass
    # print(predicates_to_list(q))
    # answer(q, '')
    #asserts
    # assert answer(('Norwegian-Dunhill', 'Marlboro-blue', 'Brit-3',
    #                'German-coffee', 'beer-white', 'cat-water',
    #                'horse-2', 'milk-3', '4-Rothmans',
    #                'dog-Swede', 'Norwegian-1', 'horse-Marlboro',
    #                'bird-Brit', '4-green', 'Winfield-beer',
    #                'Dane-blue', '5-dog', 'blue-horse',
    #                'yellow-cat', 'Winfield-Swede', 'tea-Marlboro'),
    #               'fish-color') == 'green'  # What is the color of the house where the Fish lives?
    # assert answer(('Norwegian-Dunhill', 'Marlboro-blue', 'Brit-3',
    #                'German-coffee', 'beer-white', 'cat-water',
    #                'horse-2', 'milk-3', '4-Rothmans',
    #                'dog-Swede', 'Norwegian-1', 'horse-Marlboro',
    #                'bird-Brit', '4-green', 'Winfield-beer',
    #                'Dane-blue', '5-dog', 'blue-horse',
    #                'yellow-cat', 'Winfield-Swede', 'tea-Marlboro'),
    #               'tea-number') == '2'  # What is the number of the house where tea is favorite beverage?

    # assert answer(('Norwegian-Dunhill', 'Marlboro-blue', 'Brit-3',
    #                'German-coffee', 'beer-white', 'cat-water',
    #                'horse-2', 'milk-3', '4-Rothmans',
    #                'dog-Swede', 'Norwegian-1', 'horse-Marlboro',
    #                'bird-Brit', '4-green', 'Winfield-beer',
    #                'Dane-blue', '5-dog', 'blue-horse',
    #                'yellow-cat', 'Winfield-Swede', 'tea-Marlboro'),
    #               'Norwegian-beverage') == 'water'  #  What is the favorite beverage of the Norwegian man?
    # pprint(
    # answer(('Norwegian-Dunhill', 'Marlboro-blue', 'Brit-3',
    #                'German-coffee', 'beer-white', 'cat-water',
    #                'horse-2', 'milk-3', '4-Rothmans',
    #                'dog-Swede', 'Norwegian-1', 'horse-Marlboro',
    #                'bird-Brit', '4-green', 'Winfield-beer',
    #                'Dane-blue', '5-dog', 'blue-horse',
    #                'yellow-cat', 'Winfield-Swede', 'tea-Marlboro'),
    #               'Norwegian-beverage')
    # )
    pass
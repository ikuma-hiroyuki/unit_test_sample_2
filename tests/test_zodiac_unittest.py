from unittest import TestCase

from zodiac import (
    get_zodiac_part_dict,
    get_first_month_day_of_zodiac_sign,
    create_zodiac_full_dict,
    get_zodiac_sign_name_dict,
    get_zodiac_sign_name
)


class TestGetZodiacPartDict(TestCase):
    """ get_zodiac_part_dict のテスト"""

    def test_success(self):
        """
        get_zodiac_part_dict の正常動作して正しい辞書を得られるか確認する

        エラーが発生せずに最後まで終了することを確かめる
        """

        result = get_zodiac_part_dict()

        capricorn = result['山羊座']
        self.assertEqual(capricorn['month'], 1)
        self.assertEqual(capricorn['day'], 19)

        aquarius = result['水瓶座']
        self.assertEqual(aquarius['month'], 2)
        self.assertEqual(aquarius['day'], 18)

        sagittarius = result['射手座']
        self.assertEqual(sagittarius['month'], 12)
        self.assertEqual(sagittarius['day'], 21)


class TestGetFirstMonthDayOfZodiacSign(TestCase):
    """ get_first_month_day_of_zodiac_sign のテスト """

    @classmethod
    def setUpClass(cls):
        cls.zodiac_part_dict = get_zodiac_part_dict()

    def test_month_1(self):
        """
        get_first_month_day_of_zodiac_sign の1月の正常動作を確認する
        """

        capricorn = get_first_month_day_of_zodiac_sign(1, self.zodiac_part_dict)
        self.assertDictEqual(capricorn, {'month': 12, 'day': 22})

    def test_month_2(self):
        """
        get_first_month_day_of_zodiac_sign の1月以外の塚の代表値として2月を確認する
        """

        aquarius = get_first_month_day_of_zodiac_sign(2, self.zodiac_part_dict)
        self.assertDictEqual(aquarius, {'month': 1, 'day': 20})

    def test__month_12(self):
        """
        get_first_month_day_of_zodiac_sign の12月の正常動作を確認する
        """

        sagittarius = get_first_month_day_of_zodiac_sign(12, self.zodiac_part_dict)
        self.assertDictEqual(sagittarius, {'month': 11, 'day': 22})

    def test_raise_invalid_0(self):
        """
        get_first_month_day_of_zodiac_sign に 1月未満を渡したときの異常動作を確認する
        """

        with self.assertRaises(ValueError):
            get_first_month_day_of_zodiac_sign(0, self.zodiac_part_dict)

    def test_invalid_13(self):
        """
        get_first_month_day_of_zodiac_sign に 12月超を渡したときの異常動作を確認する
        """

        with self.assertRaises(ValueError):
            get_first_month_day_of_zodiac_sign(13, self.zodiac_part_dict)


class TestCreateZodiacFullDict(TestCase):
    """ create_zodiac_full_dict のテスト """

    @classmethod
    def setUpClass(cls):
        cls.zodiac_part_dict = get_zodiac_part_dict()

    def test_success(self):
        """ create_zodiac_full_dict の正常動作を確認する """

        result = create_zodiac_full_dict(self.zodiac_part_dict)

        capricorn = result['山羊座']
        self.assertDictEqual(capricorn['from'], {'month': 12, 'day': 22})
        self.assertDictEqual(capricorn['to'], {'month': 1, 'day': 19})

        aquarius = result['水瓶座']
        self.assertDictEqual(aquarius['from'], {'month': 1, 'day': 20})
        self.assertDictEqual(aquarius['to'], {'month': 2, 'day': 18})

        sagittarius = result['射手座']
        self.assertDictEqual(sagittarius['from'], {'month': 11, 'day': 22})
        self.assertDictEqual(sagittarius['to'], {'month': 12, 'day': 21})


class TestGetZodiacSignNameDict(TestCase):
    """
    get_zodiac_sign_name_dict のテスト
    """

    @classmethod
    def setUpClass(cls):
        cls.zodiac_full_dict = create_zodiac_full_dict(get_zodiac_part_dict())

    def test_before_first_day_of_aquarius(self):
        """
        水瓶座の初日以前の日を渡して山羊座を得られるかテスト
        """

        capricorn = get_zodiac_sign_name_dict(1, 3, self.zodiac_full_dict)
        self.assertEqual(capricorn, '山羊座')

    def test_first_day_of_aquarius(self):
        """
        通常のパターンの初日を渡して水瓶座を得られるかテスト
        """

        aquarius = get_zodiac_sign_name_dict(1, 20, self.zodiac_full_dict)
        self.assertEqual(aquarius, '水瓶座')

    def test_mid_day_of_aquarius(self):
        """
        通常のパターンの中日を渡して水瓶座を得られるかテスト
        """

        aquarius = get_zodiac_sign_name_dict(1, 25, self.zodiac_full_dict)
        self.assertEqual(aquarius, '水瓶座')

    def test_last_day_of_aquarius(self):
        """
        通常のパターンの最終日を渡して水瓶座を得られるかテスト
        """

        aquarius = get_zodiac_sign_name_dict(2, 18, self.zodiac_full_dict)
        self.assertEqual(aquarius, '水瓶座')

    def test_last_day_of_capricorn(self):
        """
        年末の射手座最終日以降の日を渡して山羊座を得られるかテスト
        """

        capricorn = get_zodiac_sign_name_dict(12, 28, self.zodiac_full_dict)
        self.assertEqual(capricorn, '山羊座')

    def test_raise_invalid_month(self):
        """
        get_zodiac_sign_name_dict に 1月未満を渡したときの異常動作を確認する
        """

        with self.assertRaises(ValueError):
            get_zodiac_sign_name_dict(0, 19, self.zodiac_full_dict)


class TestGetZodiacSignName(TestCase):
    """
    get_zodiac_sign_name のテスト
    """

    @classmethod
    def setUpClass(cls):
        cls.zodiac_full_dict = create_zodiac_full_dict(get_zodiac_part_dict())

    def test_success(self):
        """
        get_zodiac_sign_name の正常動作を確認する
        """

        aquarius = get_zodiac_sign_name(1, 20)
        self.assertEqual(aquarius, '水瓶座')

        pisces = get_zodiac_sign_name(2, 29)
        self.assertEqual(pisces, '魚座')

        capricorn = get_zodiac_sign_name(12, 22)
        self.assertEqual(capricorn, '山羊座')

    def test_less_then_1(self):
        """
        get_zodiac_sign_name に 1月未満を渡したときの異常動作を確認する
        """

        with self.assertRaises(ValueError):
            get_zodiac_sign_name(0, 19)

    def test_greater_then_12(self):
        """
        get_zodiac_sign_name に 12月超を渡したときの異常動作を確認する
        """

        with self.assertRaises(ValueError):
            get_zodiac_sign_name(13, 19)

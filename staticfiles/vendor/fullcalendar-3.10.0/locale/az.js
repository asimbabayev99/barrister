! function(e, t) {
    "object" == typeof exports && "object" == typeof module ? module.exports = t(require("moment"), require("fullcalendar")) : "function" == typeof define && define.amd ? define(["moment", "fullcalendar"], t) : "object" == typeof exports ? t(require("moment"), require("fullcalendar")) : t(e.moment, e.FullCalendar)
}("undefined" != typeof self ? self : this, function(e, t) {
    return function(e) {
        function t(n) {
            if (r[n]) return r[n].exports;
            var s = r[n] = {
                i: n,
                l: !1,
                exports: {}
            };
            return e[n].call(s.exports, s, s.exports, t), s.l = !0, s.exports
        }
        var r = {};
        return t.m = e, t.c = r, t.d = function(e, r, n) {
            t.o(e, r) || Object.defineProperty(e, r, {
                configurable: !1,
                enumerable: !0,
                get: n
            })
        }, t.n = function(e) {
            var r = e && e.__esModule ? function() {
                return e.default
            } : function() {
                return e
            };
            return t.d(r, "a", r), r
        }, t.o = function(e, t) {
            return Object.prototype.hasOwnProperty.call(e, t)
        }, t.p = "", t(t.s = 189)
    }({
        0: function(t, r) {
            t.exports = e
        },
        1: function(e, r) {
            e.exports = t
        },
        189: function(e, t, r) {
            Object.defineProperty(t, "__esModule", {
                value: !0
            }), r(190);
            var n = r(1);
            n.datepickerLocale("az", "az", {
                closeText: "Закрыть",
                prevText: "&#x3C;Пред",
                nextText: "След&#x3E;",
                currentText: "Bu gün",
                monthNames: ["Yanvar", "Fevral", "Mart", "Aprel", "May", "İyun", "İyul", "Avqust", "Sentyabr", "Oktyabr", "Noyabr", "Dekabr"],
                monthNamesShort: ["Yan", "Fev", "Mar", "Apr", "May", "İyn", "İyl", "Avq", "Sen", "Okt", "Noy", "Dek"],
                dayNames: ["bazar", "bazar ertəsi", "çərşənbə axşamı", "çərşənbə", "cümə axşamı", "cümə", "şənbə"],
                dayNamesShort: ["baz", "baz.e", "ç.a", "çər", "cümə.a", "cümə", "şənb"],
                dayNamesMin: ["B", "B.e", "Ç.a", "Ç", "C.a", "C", "Ş"],
                weekHeader: "Həft",
                dateFormat: "dd.mm.yy",
                firstDay: 1,
                isRTL: !1,
                showMonthAfterYear: !1,
                yearSuffix: ""
            }), n.locale("az", {
                buttonText: {
                    month: "Ay",
                    week: "Həftə",
                    day: "Gün",
                    list: "Gündəlik"
                },
                allDayText: "Bütün gün",
                eventLimitText: function(e) {
                    return "+ daha çox " + e
                },
                noEventsMessage: "Göstərmək üçün hadisə yoxdur."
            })
        },
        190: function(e, t, r) {
            ! function(e, t) {
                t(r(0))
            }(0, function(e) {
                function t(e, t) {
                    var r = e.split("_");
                    return t % 10 == 1 && t % 100 != 11 ? r[0] : t % 10 >= 2 && t % 10 <= 4 && (t % 100 < 10 || t % 100 >= 20) ? r[1] : r[2]
                }

                function r(e, r, n) {
                    var s = {
                        ss: r ? "секунда_секунды_секунд" : "секунду_секунды_секунд",
                        mm: r ? "минута_минуты_минут" : "минуту_минуты_минут",
                        hh: "час_часа_часов",
                        dd: "день_дня_дней",
                        MM: "месяц_месяца_месяцев",
                        yy: "год_года_лет"
                    };
                    return "m" === n ? r ? "минута" : "минуту" : e + " " + t(s[n], +e)
                }
                var n = [/^янв/i, /^фев/i, /^мар/i, /^апр/i, /^ма[йя]/i, /^июн/i, /^июл/i, /^авг/i, /^сен/i, /^окт/i, /^ноя/i, /^дек/i];
                return e.defineLocale("az", {
                    months: {
                        format: "yanvar_fevral_mart_aprel_may_iyun_iyul_avqust_sentyabr_oktyabr_noyabr_dekabr".split("_"),
                        standalone: "yanvar_fevral_mart_aprel_may_iyun_iyul_avqust_sentyabr_oktyabr_noyabr_dekabr".split("_")
                    },
                    monthsShort: {
                        format: "yan._fevr._mart_apr._may_iyun_iyul_avq._sent._okt._noy._dek.".split("_"),
                        standalone: "yan._fevr._mart_apr._may_iyun_iyul_avq._sent._okt._noy._dek.".split("_")
                    },
                    weekdays: {
                        standalone: "bazar_bazar ertəsi_çərşənbə axşamı_çərşənbə_cümə axşamı_cümə_şənbə".split("_"),
                        format: "bazar_bazar ertəsi_çərşənbə axşamı_çərşənbə_cümə axşamı_cümə_şənbə".split("_"),
                        isFormat: /\[ ?[Вв] ?(?:прошлую|следующую|эту)? ?\] ?dddd/
                    },
                    weekdaysShort: "b_b.e_ç.a_ç_ç.a_c_ş".split("_"),
                    weekdaysMin: "b_b.e_ç.a_ç_ç.a_c_ş".split("_"),
                    monthsParse: n,
                    longMonthsParse: n,
                    shortMonthsParse: n,
                    monthsRegex: /^(январ[ья]|янв\.?|феврал[ья]|февр?\.?|марта?|мар\.?|апрел[ья]|апр\.?|ма[йя]|июн[ья]|июн\.?|июл[ья]|июл\.?|августа?|авг\.?|сентябр[ья]|сент?\.?|октябр[ья]|окт\.?|ноябр[ья]|нояб?\.?|декабр[ья]|дек\.?)/i,
                    monthsShortRegex: /^(январ[ья]|янв\.?|феврал[ья]|февр?\.?|марта?|мар\.?|апрел[ья]|апр\.?|ма[йя]|июн[ья]|июн\.?|июл[ья]|июл\.?|августа?|авг\.?|сентябр[ья]|сент?\.?|октябр[ья]|окт\.?|ноябр[ья]|нояб?\.?|декабр[ья]|дек\.?)/i,
                    monthsStrictRegex: /^(январ[яь]|феврал[яь]|марта?|апрел[яь]|ма[яй]|июн[яь]|июл[яь]|августа?|сентябр[яь]|октябр[яь]|ноябр[яь]|декабр[яь])/i,
                    monthsShortStrictRegex: /^(янв\.|февр?\.|мар[т.]|апр\.|ма[яй]|июн[ья.]|июл[ья.]|авг\.|сент?\.|окт\.|нояб?\.|дек\.)/i,
                    longDateFormat: {
                        LT: "H:mm",
                        LTS: "H:mm:ss",
                        L: "DD.MM.YYYY",
                        LL: "D MMMM YYYY г.",
                        LLL: "D MMMM YYYY г., H:mm",
                        LLLL: "dddd, D MMMM YYYY г., H:mm"
                    },
                    calendar: {
                        sameDay: "[Сегодня, в] LT",
                        nextDay: "[Завтра, в] LT",
                        lastDay: "[Вчера, в] LT",
                        nextWeek: function(e) {
                            if (e.week() === this.week()) return 2 === this.day() ? "[Во] dddd, [в] LT" : "[В] dddd, [в] LT";
                            switch (this.day()) {
                                case 0:
                                    return "[В следующее] dddd, [в] LT";
                                case 1:
                                case 2:
                                case 4:
                                    return "[В следующий] dddd, [в] LT";
                                case 3:
                                case 5:
                                case 6:
                                    return "[В следующую] dddd, [в] LT"
                            }
                        },
                        lastWeek: function(e) {
                            if (e.week() === this.week()) return 2 === this.day() ? "[Во] dddd, [в] LT" : "[В] dddd, [в] LT";
                            switch (this.day()) {
                                case 0:
                                    return "[В прошлое] dddd, [в] LT";
                                case 1:
                                case 2:
                                case 4:
                                    return "[В прошлый] dddd, [в] LT";
                                case 3:
                                case 5:
                                case 6:
                                    return "[В прошлую] dddd, [в] LT"
                            }
                        },
                        sameElse: "L"
                    },
                    relativeTime: {
                        future: "через %s",
                        past: "%s назад",
                        s: "несколько секунд",
                        ss: r,
                        m: r,
                        mm: r,
                        h: "час",
                        hh: r,
                        d: "день",
                        dd: r,
                        M: "месяц",
                        MM: r,
                        y: "год",
                        yy: r
                    },
                    meridiemParse: /ночи|утра|дня|вечера/i,
                    isPM: function(e) {
                        return /^(дня|вечера)$/.test(e)
                    },
                    meridiem: function(e, t, r) {
                        return e < 4 ? "ночи" : e < 12 ? "утра" : e < 17 ? "дня" : "вечера"
                    },
                    dayOfMonthOrdinalParse: /\d{1,2}-(й|го|я)/,
                    ordinal: function(e, t) {
                        switch (t) {
                            case "M":
                            case "d":
                            case "DDD":
                                return e + "-й";
                            case "D":
                                return e + "-го";
                            case "w":
                            case "W":
                                return e + "-я";
                            default:
                                return e
                        }
                    },
                    week: {
                        dow: 1,
                        doy: 4
                    }
                })
            })
        }
    })
});
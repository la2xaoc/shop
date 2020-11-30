import sqlite3
from datetime import datetime
import config
#import mysql.connector
# conn = sqlite3.connect("store.db")
# cursor = conn.cursor()

# global user1, passwords1, host1, database1
# user1 = 'root'
# passwords1 = 'godfazer'
# host1 = '127.0.0.1'
# database1 = 'store'

# conn = mysql.connector.connect(user=user1, password=passwords1, host=host1, database=database1)
# cursor = conn.cursor(buffered=True)

__connection = None

def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect("store.db")
        return __connection


conn = get_connection()
cursor = conn.cursor()


corier_list_val = []


# Додати користувача в БД
def adduser(chatid, username, firstname):
    sqlask = "INSERT INTO users(chatid, first_name, username, phonenumber, address_delivery, blocked_sender, blocked_user, status, bonus_balance) VALUES (\'{0}\', \'{1}\', \'{2}\', \'Не указан\', \'Не указан\', \'no\', \'no\', \'user\', \'0\');".format(
        str(chatid), str(firstname), str(username))
    cursor.execute(sqlask)
    conn.commit()


# Додаємо користувача в рефлист
def addUserToRefList(chid, refid):
    refer = refid.strip()
    sql = "INSERT INTO friends(chatid, friends_user) VALUES (\'{0}\', \'{1}\')".format(str(chid), str(refer))
    cursor.execute(sql)
    conn.commit()


# Кількість запрошених
def get_user_ref(chit):
    sql = 'SELECT count(*) FROM friends where friends_user = ' + str(chit)
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    if len(result) == 0:
        onliref = 0
    else:
        onliref = result[0][0]
    return onliref


# Перевірка на статус
def check_to_admin(u_id):
    sql = 'SELECT status FROM users where chatid = ' + str(u_id)
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    print(result)
    return result[0][0]


# Додаємо номер телефону в табличку юзерс
def adduserphone(chatid, phone):
    cursor.execute("UPDATE users SET phonenumber = " + str(phone) + " WHERE chatid = " + str(chatid) + ";")
    conn.commit()


# Додаємо адресу в табличку юзерс
def update_user_address(chatid, address):
    sqlask = 'UPDATE users SET address_delivery = \'' + str(address) + '\' WHERE chatid = ' + str(chatid) + ';'
    cursor.execute(sqlask)
    conn.commit()


# Отримати інформацію про користувача
def get_user_info(chatid):
    sqlask = 'SELECT first_name, phonenumber, address_delivery, bonus_balance FROM users WHERE chatid = ' + str(
        chatid) + ';'
    cursor.execute(sqlask)
    conn.commit()
    result = cursor.fetchall()
    return result


def get_brand_name(product):
    if str(product)[0:6] != 'Скидка' and str(product) != 'Bonus':
        sqlask = 'SELECT product_brand FROM product WHERE product_name = \'' + str(product) + '\';'
        cursor.execute(sqlask)
        conn.commit()
        result = cursor.fetchall()
        return result[0][0]


# Отримати баланс користувача
def getuserbalance(chid):
    sql = 'SELECT bonus_balance FROM users WHERE chatid = ' + str(chid) + ';'
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchall()
    onlibalance = result[0][0]
    return onlibalance


# Отримати кількість виставлених кристалів  юзеру
def get_crystal_user_bonus():
    sqlask = 'SELECT user_bonus FROM crystal_bonus where id = \'{0}\''.format(str(1))
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    return result[0][0]


# Отримати кількість виставлених кристалів  vip
def get_crystal_vip_bonus():
    sqlask = 'SELECT vip_bonus FROM crystal_bonus where id = \'{0}\''.format(str(1))
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    return result[0][0]

# Отримати кількість виставлених кристалів  cashback
def get_crystal_cashback_bonus():
    sqlask = 'SELECT cashback_bonus FROM crystal_bonus where id = \'{0}\''.format(str(1))
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    return result[0][0]

# Перевірка на статус vip
def check_to_vip(u_id):
    sql = 'SELECT status_vip FROM users where chatid = ' + str(u_id)
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    #print(result)
    return result[0][0]

# додаємо на баланс користувача 5 гг.
def addToMoney(chatid):
    chat_id = chatid.strip()
    print('db chat_id_user:' + chat_id)
    sql = 'UPDATE users SET bonus_balance = bonus_balance + \'{0}\' where chatid = \'{1}\''.format(str(get_crystal_user_bonus()), str(chat_id))
    cursor.execute(sql)
    conn.commit()


# додаємо на баланс vip.
def addToMoney_vip(chatid):
    chat_id = chatid.strip()
    print('db chat_id_vip:' + chat_id)
    sql = 'UPDATE users SET bonus_balance = bonus_balance + \'{0}\' where chatid = \'{1}\''.format(str(get_crystal_vip_bonus()), str(chat_id))
    cursor.execute(sql)
    conn.commit()

# додаємо на баланс cashback.
def addToMoney_cashback(chatid):
    chat_id = chatid.strip()
    print('db chat_id_cashback:' + chat_id)
    sql = 'UPDATE users SET bonus_balance = bonus_balance + \'{0}\' where chatid = \'{1}\''.format(str(get_crystal_cashback_bonus()), str(chat_id))
    cursor.execute(sql)
    conn.commit()

# Отримати статистику
def get_stat():
    users_count = get_user_count()
    users_balance = get_user_balance()
    moder_count = get_count_moder()
    users_blocked = getuserblocked()
    msg_text = 'Всего пользователей: ' + str(users_count) + '\nЗаблокировали бота: ' + str(users_blocked) \
               + '\nДенег на бонусных баллансах: ' + str(users_balance) + '\nАдминистраторов: ' + str(moder_count)
    return msg_text


def print_item(brand):
    sqlask = 'SELECT product_name FROM product WHERE product_brand = \'' + str(brand) + '\' and aviable > 0;'
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    return result


def print_itemprice(brand):
    sqlask = 'SELECT product_price FROM product WHERE product_name = \'' + str(brand) + '\' and aviable > 0;'
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    return result[0][0]


# Кількість модераторів
def get_count_moder():
    sqlask = 'SELECT COUNT(*) FROM users WHERE status = \'admin\';'
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    return result[0][0]


# Сума балансів
def get_user_balance():
    sqlask = 'SELECT SUM(bonus_balance) FROM users'
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    return result[0][0]


# Кількість підписників
def get_user_count():
    sqlask = 'SELECT COUNT(*) FROM users'
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    return result[0][0]


# Додаємо товар в корзину
def addbasket(userchatid, code_product):
    product_info = get_product_info_from_id(code_product)
    sqlask = "INSERT INTO basket(chatid, product_name, product_price, product_count) VALUES (\'{0}\', \'{1}\', \'{2}\', \'1\');".format(
        str(userchatid), str(product_info[0]), str(product_info[1]))
    cursor.execute(sqlask)
    conn.commit()


def rmbasket(userchatid, code_product):
    product_c = get_basket_count(userchatid, code_product)
    delete_product_basket(userchatid, code_product)
    product_info = get_product_info_from_id(code_product)
    i = 0
    lenasket = int(product_c) - 2
    if lenasket >= 0:
        for i in range(lenasket):
            addbasket(userchatid, code_product)
            i = + 1
        sqlask = "INSERT INTO basket(chatid, product_name, product_price, product_count) VALUES (\'{0}\', \'{1}\', \'{2}\', \'1\');".format(
            str(userchatid), str(product_info[0]), str(product_info[1]))
        cursor.execute(sqlask)
        conn.commit()
    else:
        delete_product_basket(userchatid, code_product)


def delete_product_basket(userid, product_name):
    sqlask = 'DELETE FROM basket WHERE chatid = \'{0}\' and product_name = \'{1}\';'.format(str(userid),
                                                                                            str(product_name))
    cursor.execute(sqlask)
    conn.commit()


def delete_product(product_id):
    sqlask = 'DELETE FROM product WHERE product_id = \'{0}\';'.format(str(product_id))
    cursor.execute(sqlask)
    conn.commit()


def get_basket_count(userid, product_name):
    sqlask = 'SELECT COUNT(*) FROM basket WHERE chatid = \'{0}\' and product_name = \'{1}\';'.format(str(userid),
                                                                                                     str(product_name))
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    return result[0][0]

# Количество заказаных товаров в корзине
# def get_count(chatid):
#     sql = 'SELECT COUNT(*) FROM basket WHERE chatid = \'' + str(chatid) + '\';'
#     #sql = 'SELECT COUNT(chatid) FROM basket'
#     cursor.execute(sql)
#     result = list(cursor.fetchall())
#     conn.commit()
#     return result[0][0]
# def get_count(chatid):
#     sql = 'SELECT product_name FROM basket WHERE chatid = \'' + str(chatid) + '\';'
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     conn.commit()
#     for it in result:
#         print(result)
#         if it[0] != 'Bonus' or it[0] != 'Скидка':
#             cout =+1
#     return cout
#Количество заказаных товаров в корзине
def get_count(chatid):
    sql = 'SELECT COUNT(*) FROM basket WHERE chatid = \'' + str(chatid) + '\' and product_count = 1;'
    cursor.execute(sql)
    result = list(cursor.fetchall())
    conn.commit()
    return result[0][0]


# Добавить бонус
def addbasketbonus(userchatid):
    try:
        balance = float(getuserbalance(userchatid)) * float(1)
        if balance != 0:
            sqlask = "INSERT INTO basket_bonus(chatid, product_name, product_price, product_count) VALUES (\'{0}\', \'{1}\', \'{2}\', \'2\');".format(str(userchatid), 'Bonus', str(balance))
            cursor.execute(sqlask)
            conn.commit()
            null_balance(userchatid)
    except:
        pass




# Списати з балансу
def null_balance(chatid):
    sqlask = 'UPDATE users SET bonus_balance = 0 WHERE chatid = \'' + str(chatid) + '\';'
    cursor.execute(sqlask)
    conn.commit()


# Вернуть бонус с корзины
def deladdbasketbonus(userchatid):
    try:
        update_select_bonus(userchatid)
        delete_basket_bonus(userchatid)
    except:
        pass

# Бонусы временно попадают в tmp_bonus
def tmp_deladdbasketbonus(userchatid):
    try:
        tmp_update_select_bonus(userchatid)
    except:
        pass

# Бонусы вертає з tmp_bonus
def return_deladdbasketbonus(userchatid):
    try:
        return_update_select_bonus(userchatid)
        null_update_select_bonus(userchatid)
    except:
        pass

# Дані про товар по коду
def get_product_info_from_id(name):
    sqlask = 'SELECT product_name, product_price FROM product WHERE product_name = \'' + str(name) + '\';'
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit
    return result[0]


def get_aviable_product(brand, product):
    try:
        sqlask = 'SELECT aviable FROM product WHERE product_brand = \'{0}\' and product_name = \'{1}\';'.format(
            str(brand), str(product))
        cursor.execute(sqlask)
        result = cursor.fetchall()
        conn.commit()
        return result[0][0]
    except Exception as e:
        print(e)


def get_product_info_id(code):
    sqlask = 'SELECT product_name, product_desc, product_price, product_img, product_category, product_id, aviable FROM product WHERE product_id = ' + str(code) + ' and aviable > 0;'
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    return result[0]

# Отримати назву фото
def get_photo(brand):
    sqlask = 'SELECT category_img FROM brand_photo WHERE product_brand = \'{0}\';'.format(str(brand))
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    return result[0][0]

def add_to_aviable(p_id, avi):
    sqlask = 'UPDATE product SET aviable = \'{0}\' WHERE product_id = \'{1}\';'.format(str(avi), str(p_id))
    cursor.execute(sqlask)
    conn.commit()


# Очистка корзини
def clearbasket(userchatid):
    cursor.execute("DELETE FROM basket WHERE chatid = \'" + str(userchatid) + "\';")
    conn.commit()


# Отримати список товарів в корзині (для користуваа)
def getbasketlist(userchatid):
    # operation_bonus(userchatid)
    basket = ''
    i = 0
    cursor.execute("SELECT product_name, product_price FROM basket WHERE chatid = " + str(userchatid) + ";")
    conn.commit()
    result = cursor.fetchall()
    lenbasket = len(result)
    for i in range(lenbasket):
        brand = get_brand_name(result[i][0])
        basket = basket + '\n' + str(result[i][0]) + ' ' + str(brand).replace('None', '') + ' - ' + str(
            result[i][1]) + ' тг.'
    return basket



# def skidka_bonus():
#     cursor.execute("SELECT * FROM bonus1")
#     conn.commit()
#     # cursor.execute('SELECT * FROM users where status = {admin}'.format(admin='admin'))
#     rows = cursor.fetchall()
#     print(rows)

# статус включен - yes або виключен - no
def get_bonus_status():
    sqlask = 'SELECT yes_no FROM bonus where id = \'{0}\''.format(str(1))
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    print('Скидка Статус.: ' + str(result[0][0]))
    return result[0][0]


# Отримати бонус
def get_bonus():
    #sqlask = 'SELECT * FROM bonus where skidka'
    sqlask = 'SELECT skidka FROM bonus where id = \'{0}\''.format(str(1))
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    print('Скидка: ' + str(result[0][0]))
    return result[0][0]

def basket_sort():
    sqlask = 'SELECT * FROM basket ORDER BY product_name ASC'
    cursor.execute(sqlask)
    conn.commit()

def operation_bonus(chat_id):
    status = basket_skidka(chat_id)
    mello = int(select_mello(chat_id))
    status_yes_no = get_bonus_status()
    bonus_tmp = int(get_bonus())
    print("status, mello")
    print(status, mello)
    if status == 'yes':
        #print("get_select_bonus(chatid) " + str(get_select_bonus(chat_id)))
        delete_basket(chat_id)
        #update_select_bonus(chat_id)
        #delete_basket_bonus(chat_id)

        print('delete_basket')
        if status_yes_no == 'yes':
            add_sum = (mello - 1) * bonus_tmp
            print('*************', mello, '*************')
            if mello == 2:
                #delete_basket(chat_id)
                add_basket_bonus(chat_id, 'Скидка', bonus_tmp)
            elif mello > 1:
                #delete_basket(chat_id)
                print('strp 2')
                skidka = 'Скидка'
                summ = add_sum
                add_basket_bonus(chat_id, skidka, float(summ))
            # else:
            #     delete_basket(chat_id)
        else:
            pass
    elif status == 'no':
        if status_yes_no == 'yes':
            add_sum = (mello - 1) * bonus_tmp
            if mello == 2:
                delete_basket(chat_id)
                add_basket_bonus(chat_id, 'Скидка', bonus_tmp)
            elif mello > 1:
                delete_basket(chat_id)
                skidka = 'Скидка'
                summ = add_sum
                add_basket_bonus(chat_id, skidka, float(summ))
            # else:
            #     delete_basket(chat_id)
        else:
            pass


def basket_skidka(chatid):
    sqlask = 'SELECT product_price FROM basket WHERE chatid = \'{0}\''.format(str(chatid))
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    for it in result:
        print(result)
        if float(it[0]) < 0.0:
            return 'yes'
        else:
            continue
    return 'no'


# # Отримати баланс користувача
# def getuserbalance(chid):
#     sql = 'SELECT bonus_balance FROM users WHERE chatid = ' + str(chid) + ';'
#     cursor.execute(sql)
#     conn.commit()
#     result = cursor.fetchall()
#     onlibalance = result[0][0]
#     return onlibalance

def get_select_bonus(chatid):
    product_name = 'Bonus'
    try:
        sqlask = 'SELECT product_price FROM basket_bonus WHERE chatid = \'{0}\' and product_name = \'{1}\''.format(str(chatid), product_name)
        cursor.execute(sqlask)
        conn.commit()
        result = cursor.fetchall()
        a = result[0][0]
        tmp = a
        return tmp
    except:
        pass

def get_balance_bonus(chatid):
    try:
        sqlask = 'SELECT tmp_bonus FROM users WHERE chatid = \'{0}\''.format(str(chatid))
        cursor.execute(sqlask)
        conn.commit()
        result = cursor.fetchall()
        a = result[0][0]
        tmp = a
        return tmp
    except:
        pass

#Повернення бонуса
def update_select_bonus(chatid):
    tmp = int(get_select_bonus(chatid))
    get_select_bonus1 = tmp * (1)
    print('Повернення бонуса ' + str(get_select_bonus1))
    sql = 'UPDATE users SET bonus_balance = bonus_balance + \'{0}\' where chatid = \'{1}\''.format(get_select_bonus1, str(chatid))
    cursor.execute(sql)
    conn.commit()


#Перекидує бонус временно tmp_bonus
def tmp_update_select_bonus(chatid):
    tmp = int(get_select_bonus(chatid))
    get_select_bonus1 = tmp * (1)
    print('tmp_bonus ' + str(get_select_bonus1))
    sql = 'UPDATE users SET tmp_bonus = \'{0}\' where chatid = \'{1}\''.format(get_select_bonus1, str(chatid))
    cursor.execute(sql)
    conn.commit()

#Обнуляє tmp_bonus
def null_update_select_bonus(chatid):
    get_select_bonus1 = 0
    print('tmp_bonus ' + str(get_select_bonus1))
    sql = 'UPDATE users SET tmp_bonus = \'{0}\' where chatid = \'{1}\''.format(get_select_bonus1, str(chatid))
    cursor.execute(sql)
    conn.commit()

#Перекидує бонус з tmp_bonus назад в bonus_balance
def return_update_select_bonus(chatid):
    tmp = int(get_balance_bonus(chatid))
    get_bonus = tmp * (1)
    print('tmp_bonus ' + str(get_bonus))
    sql = 'UPDATE users SET bonus_balance = bonus_balance + \'{0}\' where chatid = \'{1}\''.format(get_bonus, chatid)
    cursor.execute(sql)
    conn.commit()
    null_update_select_bonus(chatid)



# def select_mello(chatid):
#     try:
#         sqlask = 'SELECT product_name FROM basket WHERE chatid = \'{0}\''.format(str(chatid))
#         cursor.execute(sqlask)
#         result = cursor.fetchall()
#         conn.commit()
#         mello = 0
#         getlen = len(result) - 1
#         print(getlen)
#         for ml in range(getlen):
#             print(ml, result[ml], result[ml][0])
#             print('select_mello ' + str(result[ml][0])[0:1])
#             if str(result[ml][0])[0:6] != 'Скидка' and str(result[ml][0] != 'Bonus'):
#                 brand = get_brand_name(result[ml][0])
#                 cagegoty = get_category_product_name(result[ml][0])
#                 if brand == 'MELLO' and cagegoty == 'Подгузники':
#                     mello += 1
#                 else:
#                     continue
#             ml += 1
#         return mello
#     except Exception as e:
#         print('select_mello select error', e)

def select_mello(chatid):
    try:
        mello = 0
        cursor.execute("SELECT product_name, product_price FROM basket WHERE chatid = " + str(chatid) + ";")
        conn.commit()
        result = cursor.fetchall()
        lenbasket = len(result)
        print('result ' + str(result))
        print('result ' + str(lenbasket))
        for i in range(lenbasket):
            brand = get_brand_name(result[i][0])
            cagegoty = get_category_product_name(str(result[i][0]))
            print('select_brand_1 ' + str(brand))
            print('select_cagegoty ' + str(cagegoty))
            if brand == 'MELLO' and cagegoty == 'Подгузники':
                mello += 1
        print('select_mello ' + str(mello))
        return mello
    except Exception as e:
        print('select_mello select error', e)

def add_basket_bonus(userid, product_name, product_price):
    print(userid, product_name, product_price)
    sqlask = "INSERT INTO basket_skidka(chatid, product_name, product_price, product_count) VALUES (\'{0}\', \'{1}\', \'{2}\', \'2\');".format(
        str(userid), str(product_name), float(product_price))
    cursor.execute(sqlask)
    conn.commit()
    print('ok')

def delete_basket_bonus(userid):
    print('delete Bonus')
    product_name = 'Bonus'
    try:
        #sqlask = 'DELETE FROM basket WHERE product_price < 0.0 and chatid = \'{0}\''.format(userid)
        sqlask = 'DELETE FROM basket_bonus WHERE chatid = \'{0}\' and product_name = \'Bonus\''.format(userid)
        cursor.execute(sqlask)
        conn.commit()
    except Exception as e:
        print('delete error: ', e)


# def delete_basket(userid):
#     print('delete Скидка')
#     product_name = 'Скидка'
#     try:
#         #sqlask = 'DELETE FROM basket WHERE product_price < 0.0 and chatid = \'{0}\''.format(userid)
#         sqlask = 'DELETE FROM basket WHERE product_price < 0.0 and chatid = \'{0}\' and product_name = \'{1}\''.format(userid, product_name)
#         cursor.execute(sqlask)
#         conn.commit()
#     except Exception as e:
#         print('delete error: ', e)

def delete_basket(userid):
    print('delete Скидка')
    product_name = 'Скидка'
    try:
        sqlask = 'DELETE FROM basket_skidka WHERE product_name = \'Скидка\' and chatid = \'{0}\''.format(userid)
        cursor.execute(sqlask)
        conn.commit()
    except Exception as e:
        print('delete error: ', e)


def get_basket_name(chatid):
    basket = []
    cursor.execute("SELECT product_name FROM basket WHERE chatid = " + str(chatid) + ";")
    conn.commit()
    result = cursor.fetchall()
    for item in result:
        basket.append(item[0])
    return basket

# bonusprice_text Скидка, Бонуси
def bonusprice_text(userchatid):
    bonusprice = basket_bonus_all(userchatid)
    basket_b = basket_bonus(userchatid)
    if bonusprice and basket_b:
        bonusprice_text = '\nСкидка - -' + str(bonusprice) + '\nБонус - -' + str(basket_b)
    elif basket_b:
        bonusprice_text = '\nБонус - -' + str(basket_b)
    elif bonusprice:
        bonusprice_text = '\nСкидка - -' + str(bonusprice)
    else:
        bonusprice_text = ''
    return bonusprice_text




# Отримуємо загальну ціну товарів в корзині Всего -
def selectallprice1(userchatid):
    allprice = 0
    i = 0
    cursor.execute("SELECT product_price FROM basket WHERE chatid = " + str(userchatid) + ";")
    conn.commit()
    result = cursor.fetchall()
    lenbasket = len(result)
    for i in range(lenbasket):
        allprice = allprice + float(result[i][0])
        i += 1
    bonusprice = basket_bonus_all(userchatid)
    basket_b = basket_bonus(userchatid)
    allprice = allprice - bonusprice - basket_b
    return allprice


# Отримуємо загальну ціну товарів в корзині Всего -
def selectallprice(userchatid):
    allprice = 0
    cursor.execute("SELECT product_price FROM basket WHERE chatid = " + str(userchatid) + ";")
    conn.commit()
    result = cursor.fetchall()
    lenbasket = len(result)
    for i in range(lenbasket):
        allprice = allprice + float(result[i][0])
        i += 1
    bonusprice = float(basket_bonus_all(userchatid))
    basket_b = float(basket_bonus(userchatid))
    if bonusprice:
        allprice = allprice - bonusprice - basket_b
        return allprice
    elif basket_b:
        allprice = allprice - basket_b
        return allprice
    else:
        allprice = 0
        cursor.execute("SELECT product_price FROM basket WHERE chatid = " + str(userchatid) + ";")
        conn.commit()
        result = cursor.fetchall()
        lenbasket = len(result)
        for i in range(lenbasket):
            allprice = allprice + float(result[i][0])
            i += 1
        return allprice

# Отримуємо загальну ціну скидки в корзині Всего -
def basket_bonus_all(userchatid):
    allprice = 0
    i = 0
    cursor.execute("SELECT product_price FROM basket_skidka WHERE chatid = " + str(userchatid) + ";")
    conn.commit()
    result = cursor.fetchall()
    lenbasket = len(result)
    for i in range(lenbasket):
        allprice = allprice + float(result[i][0])
        i += 1
    return allprice

# Отримуємо загальну ціну бонусів в корзині Всего -
def basket_bonus(userchatid):
    allprice = 0
    i = 0
    cursor.execute("SELECT product_price FROM basket_bonus WHERE chatid = " + str(userchatid) + ";")
    conn.commit()
    result = cursor.fetchall()
    lenbasket = len(result)
    for i in range(lenbasket):
        allprice = allprice + float(result[i][0])
        i += 1
    return allprice


# Отримуємо номер телефону користуваа
def getuserphone(userid):
    cursor.execute("SELECT phone FROM users WHERE chatid = " + str(userid) + ";")
    conn.commit()
    result = cursor.fetchall()
    phonenum = result[0][0]
    return phonenum


# Додати замовлення в базу
def addorders(chatid, price, status):
    print(status)
    date_today = str(datetime.now().date())
    sqlask = "INSERT INTO orders(datetime, chatid, price, status) VALUES (\'{0}\', \'{1}\', {2}, \'{3}\');".format(
        date_today, str(chatid), str(price), str(status))
    cursor.execute(sqlask)
    conn.commit()


def update_orders_status(chatid, status):
    print(chatid, status)
    try:
        sqlask = "UPDATE orders SET status = \'{0}\' WHERE chatid = \'{1}\';".format(str(status), str(chatid))
        cursor.execute(sqlask)
        conn.commit()
    except Exception as e:
        print(e)


# Отримуємо загальну кількість людей в базі
def getallusersstodb():
    listusers = []
    sql = 'SELECT * FROM users'
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in result:
        listusers.append(i)
    quser = len(listusers)
    return quser


# Отримуємо список користувачів які не заблокували розсилку
def dontblockssender():
    listusers = []
    sql = 'SELECT id FROM users WHERE blockedsender = 0'
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchall()
    for i in result:
        listusers.append(i)
    quser = len(listusers)
    return quser


# Перевірка користувача на унікальність
def checkunicusers(usr):
    sql = 'SELECT chatid FROM users WHERE chatid = ' + str(usr)
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchall()
    return result


# Позначаємо користувача як "заблокував"
def blockedsenderadd(usr):
    sql = 'UPDATE users SET blocked_sender = \'yes\' WHERE chatid = ' + str(usr)
    cursor.execute(sql)
    conn.commit()


# Кількість підписників
def allsub():
    sql = 'SELECT COUNT(chatid) FROM users'
    cursor.execute(sql)
    result = list(cursor.fetchall())
    conn.commit()
    return result[0][0]


# заблокували підписку
def getuserblocked():
    sql = 'SELECT count(chatid) FROM users WHERE blocked_sender = \'yes\''
    cursor.execute(sql)
    result = list(cursor.fetchall())
    conn.commit()
    statususer = result[0][0]
    return statususer


# Оновити доставку
def insert_dlv_type(chid):
    sql = 'INSERT INTO delivery_type(chatid, type_dlv) VALUES (\'{0}\', \'none\');'.format(str(chid))
    cursor.execute(sql)
    conn.commit()


def update_dlv_type(chid, data):
    sql = 'UPDATE delivery_type SET type_dlv = \'{0}\' WHERE chatid = \'{1}\';'.format(str(data), str(chid))
    cursor.execute(sql)
    conn.commit()


def get_dlv_type(chatid):
    sqlask = 'SELECT type_dlv FROM delivery_type'
    cursor.execute(sqlask)
    conn.commit()
    result = cursor.fetchall()
    return result[0][0]


# adminstat
def day_orders_count():
    sttime = str(datetime.now().date())
    sqlask = 'SELECT COUNT(*) FROM orders WHERE datetime = \'{0}\';'.format(sttime)
    cursor.execute(sqlask)
    conn.commit()
    result = cursor.fetchall()
    return result[0][0]


def day_orders_summ():
    sttime = str(datetime.now().date())
    sqlask = 'SELECT SUM(price) FROM orders WHERE datetime = \'{0}\';'.format(sttime)
    cursor.execute(sqlask)
    conn.commit()
    result = cursor.fetchall()
    return result[0][0]


# Зміна статусу користувача
def edit_user_status(userid, status):
    sqlask = 'UPDATE users SET status = \'{0}\' WHERE chatid = \'{1}\';'.format(str(status), str(userid))
    cursor.execute(sqlask)
    conn.commit()


def get_end_id():
    sqlask = 'SELECT product_id FROM product'
    cursor.execute(sqlask)
    list_res = cursor.fetchall()
    conn.commit()
    getlen = len(list_res)
    result = list_res[getlen - 1][0]
    return result


def add_item_db(name, desc, price, category, brand, aviable):
    product_id = int(get_end_id()) + 1
    sqlask = 'INSERT INTO product(product_id, product_name, product_desc, product_img,' + \
             'product_price, product_category, product_brand, aviable) VALUES (\'{0}\', \'{1}\', \'{2}\', \'none\', \'{3}\', \'{4}\', \'{5}\', {6});'.format(
                 str(product_id), str(name), str(desc), str(price), str(category), str(brand), aviable)
    cursor.execute(sqlask)
    conn.commit()


def count_item():
    sqlask = 'SELECT COUNT(*) FROM product'
    cursor.execute(sqlask)
    conn.commit()
    result = cursor.fetchall()
    return result[0][0]


def select_cat(category):
    sqlask = 'SELECT text FROM textdata WHERE category = \'{0}\';'.format(str(category))
    cursor.execute(sqlask)
    conn.commit()
    result = cursor.fetchall()
    return result[0][0]


def update_cat(cat, text):
    sqlask = 'UPDATE textdata SET text = \'{0}\' WHERE category = \'{1}\';'.format(str(text), str(cat))
    print(sqlask)
    cursor.execute(sqlask)
    conn.commit()


def edit_product(id_p, edit_name, edit_val):
    sqlask = 'UPDATE product SET ' + str(edit_name) + ' = \'' + str(edit_val) + \
             '\' WHERE product_id = \'' + str(id_p) + '\';'
    cursor.execute(sqlask)
    conn.commit()

#Дадає або змінює фото в тиблиці brand_photo по назві бренду, бренд не має повторюватись
def edit_photo(category_img, product_brand):
    try:
        sqlask = 'UPDATE brand_photo SET category_img = \'{0}\' WHERE product_brand = \'{1}\';'.format(str(category_img), str(product_brand))
        cursor.execute(sqlask)
        conn.commit()
    except:
        print('except')


def get_all_product():
    sqlask = 'SELECT * FROM product'
    cursor.execute(sqlask)
    conn.commit()
    result = cursor.fetchall()
    return result


def select_users():
    sqlask = 'SELECT chatid FROM users'
    cursor.execute(sqlask)
    conn.commit()
    result = cursor.fetchall()
    return result


def add_sender(text, status):
    datetoday = str(datetime.today().date())
    sqlask = 'INSERT INTO sender(date, text, status) VALUES (\'{0}\', \'{1}\', \'{2}\');'.format(datetoday, str(text),
                                                                                                 str(status))
    cursor.execute(sqlask)
    conn.commit()
    conn.close()


def select_draf():
    sqlask = 'SELECT * FROM sender WHERE status = \'Черновик\';'
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    return result


def select_send():
    sqlask = 'SELECT * FROM sender WHERE status = \'Отправлено\';'
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    return result


def delete_draf(text):
    sqlask = 'DELETE FROM sender WHERE text = \'{0}\';"'.format(str(text))
    cursor.execute(sqlask)
    conn.commit()


def delete_send(text):
    sqlask = 'DELETE FROM sender WHERE text = \'{0}\';"'.format(str(text))
    cursor.execute(sqlask)
    conn.commit()


def select_history(chatid):
    sqlask = 'SELECT * FROM history WHERE chatid = \'{0}\';'
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    return result


def add_history(chatid, product_name, product_price, datetime, status):
    datetodat = datetime.today().date()
    sqlask = 'INSERT INTO history(chatid, product_name, product_price, datetime, status) VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\');'.format(
        str(chatid), \
        str(product_name), str(product_price), str(datetodat), str(status))
    cursor.execute(sqlask)
    conn.commit()


def select_admin1():
    global temp
    cursor.execute("SELECT * FROM users")
    #cursor.execute('SELECT * FROM users where status = {admin}'.format(admin='admin'))
    rows = cursor.fetchall()
    for j in rows:
        if 'admin' == j[7]:
            temp = j[0]
            print(str(temp) + ' ADMIN')
            result = temp
    return result




def select_admin():
    sqlask = 'SELECT chatid FROM users where status = \'admin\''
    cursor.execute(sqlask)
    result = cursor.fetchall()
    print(str(result))
    conn.commit()
    return result


def select_man():
    sqlask = 'SELECT chatid FROM users where status = \'manager\''
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    return result


def select_cur():
    sqlask = 'SELECT chatid FROM users where status = \'courier\''
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    return result


def courier_list():
    sqlask = 'SELECT chatid, first_name FROM users where status = \'courier\''
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    getlen = len(result)
    return_rz = []
    for i in range(getlen):
        return_rz.append(result[i][0])
        return_rz.append(result[i][1])
        i += 1
    return return_rz


def select_friend_user(chatid):
    sqlask = 'SELECT friends_user FROM friends WHERE chatid = \'{0}\';'.format(str(chatid))
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    return result[0][0]


def get_address_user(chatid):
    sqlask = 'SELECT address_delivery FROM users WHERE chatid = \'{0}\';'.format(str(chatid))
    cursor.execute(sqlask)
    resutl = cursor.fetchall()
    conn.commit()
    return resutl[0][0]


def get_phone_user(chatid):
    sqlask = 'SELECT phonenumber FROM users WHERE chatid = \'{0}\';'.format(str(chatid))
    cursor.execute(sqlask)
    resutl = cursor.fetchall()
    conn.commit()
    return resutl[0][0]


def get_count_item(chatid, product_name):
    sqlask = 'SELECT COUNT(*) FROM basket WHERE chatid = \'{0}\' and product_name = \'{1}\';'.format(str(chatid),
                                                                                                     str(product_name))
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    return result[0][0]


def get_all_brand(category):
    sqlask = 'SELECT product_brand FROM product WHERE product_category = \'{0}\';'.format(str(category))
    cursor.execute(sqlask)
    brand = cursor.fetchall()
    conn.commit()
    result = []
    for br in brand:
        if br not in result:
            result.append(br)
    return result


def get_br():
    sqlask = 'SELECT product_brand FROM product'
    cursor.execute(sqlask)
    lst = cursor.fetchall()
    conn.commit()
    result = []
    for rez in lst:
        if rez[0] not in result:
            result.append(rez[0])
    return result


def get_category_product_name(product):
    sqlask = 'SELECT product_category FROM product WHERE product_name = \'{0}\';'.format(str(product))
    cursor.execute(sqlask)
    name = cursor.fetchall()
    conn.commit()
    return name[0][0]


def get_category_name(brand):
    sqlask = 'SELECT product_category FROM product WHERE product_brand = \'{0}\';'.format(str(brand))
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    name = ''
    for item in result:
        name = item
        break
    return name[0]


def aviable_minus(product_name):
    try:
        sqlask = 'UPDATE product SET aviable = aviable - 1 WHERE product_name = \'{0}\';'.format(str(product_name))
        cursor.execute(sqlask)
        conn.commit()
    except:
        print('except')


def get_id_pd():
    sqlask = 'SELECT product_id FROM product'
    cursor.execute(sqlask)
    conn.commit()
    result = cursor.fetchall()
    output = []
    for i in result:
        output.append(i[0])
    return output


def get_name_pd():
    sqlask = 'SELECT product_name FROM product'
    cursor.execute(sqlask)
    conn.commit()
    result = cursor.fetchall()
    output = []
    for i in result:
        output.append(i[0])
    return output


def get_desc_pd():
    sqlask = 'SELECT product_desc FROM product'
    cursor.execute(sqlask)
    conn.commit()
    result = cursor.fetchall()
    output = []
    for i in result:
        output.append(i[0])
    return output


def get_price_pd():
    sqlask = 'SELECT product_price FROM product'
    cursor.execute(sqlask)
    conn.commit()
    result = cursor.fetchall()
    output = []
    for i in result:
        output.append(i[0])
    return output


def get_category_pd():
    sqlask = 'SELECT product_category FROM product'
    cursor.execute(sqlask)
    conn.commit()
    result = cursor.fetchall()
    output = []
    for i in result:
        output.append(i[0])
    return output


def get_brand_pd():
    sqlask = 'SELECT product_brand FROM product'
    cursor.execute(sqlask)
    conn.commit()
    result = cursor.fetchall()
    output = []
    for i in result:
        output.append(i[0])
    return output


def get_aviable_pd():
    sqlask = 'SELECT aviable FROM product '
    cursor.execute(sqlask)
    conn.commit()
    result = cursor.fetchall()
    output = []
    for i in result:
        output.append(i[0])
    return output


def delete_endmenu(usserid):
    sqlask = 'DELETE FROM end_menu WHERE chatid = \'{0}\';'.format(str(usserid))
    cursor.execute(sqlask)
    conn.commit()


def insert_endmenu(userid, menu):
    try:
        delete_endmenu(userid)
        sqlask = 'INSERT INTO end_menu(chatid, menu) VALUES (\'{0}\', \'{1}\');'.format(str(userid), str(menu))
        cursor.execute(sqlask)
        conn.commit()
    except:
        sqlask = 'INSERT INTO end_menu(chatid, menu) VALUES (\'{0}\', \'{1}\');'.format(str(userid), str(menu))
        cursor.execute(sqlask)
        conn.commit()


def select_endmenu(userid):
    sqlask = 'SELECT menu FROM end_menu WHERE chatid = \'{0}\';'.format(str(userid))
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    return result[0][0]

#Отримаємо кількість в БД сьогоднішньої дати
def get_count_idorder():
    date_td = datetime.today().date()
    #sqlask = 'SELECT COUNT() FROM id_orders WHERE data = \'{0}\''.format(str(date_td))
    sqlask = 'SELECT COUNT() FROM id_orders WHERE data_year = \'{0}\''.format(str(date_td.year))
    cursor.execute(sqlask)
    result = cursor.fetchall()
    conn.commit()
    print('Year ' + str(date_td.year))
    print('get_count_idorder() ' + str(result[0][0]))
    return result[0][0]

#Записуєм в базу сьогоднішню дату і номер
def insert_id_order():
    date_td = datetime.today().date()
    count = get_count_idorder()
    newid = int(count) + 1
    sqlask = 'INSERT INTO id_orders(data_year, data, id) VALUES (\'{0}\', \'{1}\', \'{2}\');'.format(str(date_td.year), str(date_td), str(newid))
    print(sqlask)
    cursor.execute(sqlask)
    conn.commit()

#Отримаємо номер заказа
def select_end_oid():
    insert_id_order()
    date_td = datetime.today().date()
    print(date_td)
    sqlask = 'SELECT id FROM id_orders WHERE data_year = \'{0}\''.format(str(date_td.year))
    cursor.execute(sqlask)
    result = cursor.fetchall()
    print(result)
    conn.commit()
    rzz = []
    for rz in result:
        rzz.append(rz[0])
    print(rzz)
    return rzz[-1]


def insert_msgid(chatid, msg_id):
    sqlask = 'INSERT INTO lastmsg_id(chatid, msg_id) VALUES (\'{0}\', \'{1}\');'.format(str(chatid), str(msg_id))
    cursor.execute(sqlask)
    conn.commit()


def select_end_msgid(msg_id):
    try:
        sqlask = 'SELECT msg_id FROM lastmsg_id WHERE chatid = \'{0}\''.format(str(msg_id))
        cursor.execute(sqlask)
        result = cursor.fetchall()
        conn.commit()
        return result[0][0]
    except:
        return 'none'


def insert_comment(chatid, comment):
    print(chatid, comment)
    try:
        sqlask = 'INSERT INTO user_comment(chatid, comment) VALUES (\'{0}\', \'{1}\');'.format(str(chatid),
                                                                                               str(comment))
        cursor.execute(sqlask)
        conn.commit()
    except Exception as e:
        print(e)


def select_comment(chatid):
    try:
        sqlask = 'SELECT comment FROM user_comment WHERE chatid = \'{0}\';'.format(str(chatid))
        cursor.execute(sqlask)
        result = cursor.fetchall()
        conn.commit()
        print(result[0][0])
        return result[0][0]
    except:
        return 'none'


def delete_comment(chatid):
    try:
        sqlask = 'DELETE FROM user_comment WHERE chatid = \'{0}\';'.format(str(chatid))
        cursor.execute(sqlask)
        conn.commit()
    except:
        pass




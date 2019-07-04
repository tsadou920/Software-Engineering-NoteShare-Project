procedure Approve_membership(email)
    Assert email is valid
        return ("Invalid email!")
    If email is in user_DB then
        return ("User already exists!")
    user_DB.add_record(email)
    send request to create password
    return ("User was added successfully and notified!")
  end

procedure Ban_user(userId)
    Assert userId is valid
        return("Invalid userId!")
    If userId is in user_DB then
        set to_ban to user_DB.pop(userId)
        banned_users.add(userId)
        return ("User was sucessfully banned.")
    return ("User is not in the user_DB")

procedure Taboo_word(word)
    Asssert word is valid
        return("Invalid word format!")
    If word is in the taboo_DB then
        return("Word already banned!")
    taboo_DB.add(word)
    return("Word banned successfully!")

procedure Taboo_suggested_word(word)
    call Taboo_word(word)

procedure Remove_from_taboo(word)
    Assert word is valid
        return("Invalid word format!")
    If word is in taboo_DB then

procedure 
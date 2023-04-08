import manage__prods
import manage__users
import manage_carts
import total_functions


def main_menu():
    while True:
        main_choice = input("What collection do you want to work with? (Users / Carts / Products / Total / Quit): ")
        if main_choice == "Products":
            manage__prods.show__products()
        elif main_choice == "Users":
            manage__users.show__users(queryType="general")
        elif main_choice == "Carts":
            manage_carts.show__carts_operation()
        elif main_choice == "Total":
            total_functions.show_total_options()
        elif main_choice == "Quit":
            break
        else:
            print("Invalid choice. Please try again.")
# block to allow the code to be imported without running the main_menu() function.
if __name__ == "__main__":
    main_menu()
#Importing ABC to have access to @abtractmethod in order to hide complexity of certain methods
from abc import ABC, abstractmethod

class Product():
    #Initializing product_id, name, price, quantity
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
    
    #Method update_quantity sets new_quantity to old quanitity, quantity is how much of a certain object exists, doesn't create multiples of that object
    def update_quantity(self, new_quantity):
        self.quantity = new_quantity

    #Method get_product_info prints out attribute information, as well as calculate price which takes into account of quantity of a certain product
    def get_product_info(self):
        print(f'Name: {self.name}')
        print(f'Price: ${self.price*self.quantity} (${self.price}/Unit)')
        print(f'Quantity: {self.quantity}')
        print(f'Product ID: {self.product_id}')
    
#Inheritance of Product
class DigitalProduct(Product):
    #Initializing file_size and download_link
    def __init__(self, file_size, download_link, product_id, name, price, quantity):
        #Inheriting attributes from Product (product_id, name, price, quantity) using super() to initialize
        super().__init__(product_id, name, price, quantity)
        self.file_size = file_size
        self.download_link = download_link

    #Method get_product_info prints out product info with Product inheritance
    def get_product_info(self):
        '''print(f'Name: {self.name}')
        print(f'Price: {self.price}')
        print(f'Quantity: {self.quantity}')'''
        #Super() is used to call get_product_info() in Product class
        super().get_product_info()
        #These lines overide the function making this certain get_product_info() unique to DigitalProduct
        print(f'Product ID: {self.product_id}')
        print(f'File Size: {self.file_size}')
        print(f'Downlaod Link: {self.download_link}\n')


class PhysicalProduct(Product):
    #Initializing weight, dimensions
    def __init__(self, weight, dimensions, product_id, name, price, quantity):
        #Inheriting attributes from Product (product_id, name, price, quantity) using super() to initialize
        super().__init__(product_id, name, price, quantity)
        self.weight = weight
        self.dimensions = dimensions

    #Method get_product_info prints out product info with Product inheritance
    def get_product_info(self):
        '''print(f'Name: {self.name}')
        print(f'Price: {self.price}')
        print(f'Quantity: {self.quantity}')'''
        #Super() is used to call get_product_info() in Product class
        super().get_product_info()
        #These lines overide the function making this certain get_product_info() unique to PhysicalProduct
        print(f'Weight: {self.weight}')
        print(f'Dimensions: {self.dimensions}\n')

#Abstract Cart inherits ABC to used @abstractmethod
class AbstractCart(ABC):
    #Using abstraction to hide the complexity of methods from user, methods are used later on in Cart class
    @abstractmethod
    def add_product(self, product):
        pass

    @abstractmethod
    def remove_product(self, product_id):
        pass
    
    @abstractmethod
    def view_cart(self):
        pass
    
    @abstractmethod
    def calculate_total(self):
        pass
    
    @abstractmethod
    def clearCart(self):
        pass


#Inherits Product and AbstractCart classes
class Cart(Product, AbstractCart):
    #Initializing cart_items (a list that will contain Product objects) which is a private attribute
    def __init__(self, cart_items):
        self.__cart_items = cart_items

    #add_product method appends product objects into cart_items 
    def add_product(self, product):
        self.__cart_items.append(product)

    #remove_product method removes certain objects from cart_items by comparing product_id
    def remove_product(self, product_id):
        #Loops through cart_items
        for i in self.__cart_items:
            #If Product object matches with provided product_id then if conditional activates and removes said object from list/cart_items
            if i.product_id:
                self.__cart_items.remove(i)
        print(f'{product_id} was removed from the cart.\n')
        
    #view_cart method loops through cart_items and uses get_product_info() method from Product class to print out info
    #It also used polymorphism because it can differentiate if it is a DigitalProduct object and a PhysicalProduct object in order to use specific get_product_info() methods
    def view_cart(self):
        for i in self.__cart_items:
            i.get_product_info()

    #calculate_total method loops through cart_items and adds price*quantity (attributes that Product objects have) to total
    def calculate_total(self):
        total = 0
        for i in self.__cart_items:
            total+=i.price*i.quantity
        return total
        #print(f'Total Cost: {total}')

    #clearCart method just clears the cart, this is used in checkout() later on
    def clearCart(self):
        self.__cart_items.clear()
        print(f'The cart is empty.')
            

#Discount inherits ABC in order to use @abstractmethod to hide discount complexity from user
class Discount(ABC):
    @abstractmethod
    def apply_discount(total_amount):
        pass

#PercentageDiscount inherits Discount
class PercentageDiscount(Discount):
    #Initialize percentage
    def __init__(self, percentage):
        self.percentage = percentage

    #apply_discount method returns the total price after the discount percentage is applied to the total
    def apply_discount(self, total_amount):
       return total_amount - (total_amount*self.percentage)

#FixedAmountDiscount inherits Discount
class FixedAmountDiscount(Discount):
    #Initialize amount
    def __init__(self, amount):
        self.amount = amount

    #apply_discount method returns the total price after the fixed amount discount is applied to the total
    def apply_discount(self, total_amount):
        return total_amount-self.amount

#Abstraction is already used in Cart class to hide complexity from user
class User():
    #Initializes user_id, name, and an instance of the Cart class as cart
    def __init__(self, user_id, name, cart):
        self.user_id = user_id
        self.cart = cart
        self.name = name
        #Instance of discount is initialized in order to apply discount class in checkoust()
        self.discount = None

    #add_to_cart method adds Product objects in the users Cart classes cart_items
    def add_to_cart(self, product):
        #Since cart is an instance of the Cart class it may use the add_product() method to append a Product obejct into cart_items
        self.cart.add_product(product)

    #remove_from_cart method removes Product objects in the users Cart classes cart_items
    def remove_from_cart(self, product_id):
        #Since cart is an instance of the Cart class it may use the remove_product() method to remove a Product obejct from cart_items
        self.cart.remove_product(product_id)

    #checkout method prints out total after discounts are applied
    def checkout(self):
        #total equals to the carts Cart class method calculate_total() which is just price*quantity
        total = self.cart.calculate_total()
        #if statement triggers if a discount is detected in User class when created in testing
        if self.discount:
            #total equals to discount Discount classes apply_discount() method, uses polymorphism by determining if it is a PercentageDiscount or FixedAmountDiscount
            #then it will select that specific apply_discount() method accordingly from the specific class
            total = self.discount.apply_discount(total) 
            print(f'Discounted Total: ${total}')
            #Clears cart using Cart class clearCart() method
            self.cart.clearCart()
        #else statement triggers if discount still remains None and is not detected
        else:
            print(f'Total Price: ${total}')
            #Clears cart using Cart class clearCart() method
            self.cart.clearCart()

#Testing

#2 instances of DigitalProduct and 3 instances of PhysicalProduct with appropriate attributes
VideoGame = DigitalProduct('80GB', 'www.videogamedownload.com', 'GTA V', 'GTA V', 80, 1)
Subscription = DigitalProduct('5GB', 'www.streamingservice.com', 'Netflix', 'Netflix', 20, 1)
Rice = PhysicalProduct('50 ibs', '16 in x 36 in', 'White Rice', 'White Rice', 40, 1)
Beans = PhysicalProduct('3 ibs', '4 in x 5 in', 'Black Beans', 'Black Beans', 5, 1)
Cereal = PhysicalProduct('5 ibs', '6 in x 12 in', 'Frosted Flakes', 'Frosted Flakes', 10, 1)

#2 instances of userCarts are made in order to provide each user with a cart to shop with, each cart starts off empty
user1Cart = Cart([])
user2Cart = Cart([])

#2 instances of users, one named user1 and the other user 2. Provided in the third parameter are the carts created previously.
user1 = User(1, 'Eric', user1Cart)
user2 = User(2, 'Jason', user2Cart)

#user1 gets the digital products added into their cart
#since user1 is a User class it has access to the add_to_cart() method which has access to the add_product() method in the Cart class
#furthermore, the add_product() method differentiates that it is adding a DigitalProduct object so it uses DigitalProducts class add_product() method
user1.add_to_cart(VideoGame)
user1.add_to_cart(Subscription)

#view_cart() method from Cart class prints out the cart of user1 after adding on VideoGame and Subscription DigitalProduct objects
#user1.cart.view_cart()

#Instance of PercentageDiscount is created named PercDisc1, with a given percentage of 0.2
PercDisc1 = PercentageDiscount(0.2)
#Since User class calculates checkout total user1 is given the discount PercDisc1
user1.discount = PercDisc1

#This print statement is to check the Encapsulation of cart_items and makes sure that it is a private attribute
print(user1Cart.__cart_items)

#user1 checkout() method check, ensures that discounts are applied
user1.checkout()
#Makes sure that the cart is clear after checkout
user1.cart.view_cart()

Rice.get_product_info()
#Testing update_quantity() method, making the Rice quantity 2 instead of 1 
Rice.update_quantity(2)
#Testing get_product_info() method, prints out the information of Rice after the quantity change
Rice.get_product_info()

#Testing Cart class

#Testing add_product() method to add Rice into user2Carts cart
user2Cart.add_product(Rice)
#Checking to make sure Rice was added into user2Cart, as well as checking if view_cart() method works
user2Cart.view_cart()
#Testing calculate_total() method from Cart class, so far it would calculate the total price for 2 Rice objects 
print(user2Cart.calculate_total())
#Testing remove_product() method from Cart class, 'White Rice' is removed
user2Cart.remove_product('White Rice')
#Verifying that Rice object has been removed from user2Cart, so cart should be empty
user2Cart.view_cart()
#This print statement is to check the Encapsulation of cart_items and makes sure that it is a private attribute
print(user2Cart.__cart_items)

#Testing User class

#Testing add_to_cart() method, PhysicalProduct like Rice, Beans, and Cereal objects are added to user2
user2.add_to_cart(Rice)
user2.add_to_cart(Beans)
user2.add_to_cart(Cereal)
#Verifying the method by checking user2s cart using Cart class view_cart() method
user2.cart.view_cart()

#Testing remove_from_cart() method by providing product_id
user2.remove_from_cart('Black Beans')
#Verifying the method by checking user2s cart using Cart class view_cart() method
user2.cart.view_cart()

#Instance of FixedAmountDiscount is created named PercDisc2, with a given fixed amount 10
PercDisc2 = FixedAmountDiscount(10)
#Since User class calculates checkout total user2 is given the discount PercDisc2
user2.discount = PercDisc2

#user2 checkout() method check, ensures that discounts are applied
user2.checkout()
#Makes sure that the cart is clear after checkout
user2.cart.view_cart()

#Test to make sure discount cannot be instantiated directly, basically this throws an error
AbstractDiscountTest = Discount(10)

window.onload = function(){

    const priceSetup = () => {
        let priceSpans = document.getElementsByClassName('productSubTotal')
        let priceArray = []
        Array.from(priceSpans).forEach(e=>{
            priceElem = Number.parseFloat(e.innerHTML)
            priceArray.push(priceElem)
        })
        let result = priceArray.reduce((a,b) => {
            return a + b
        })

        document.getElementById('priceTotal').innerHTML = result

        document.getElementById('totalAmount').innerHTML = result + 1

    }

    priceSetup()

    $('.qty-plus').click(function(){
        let qtyElem = this.parentElement.parentElement.children[1]
        let productBox = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement
        let productSub = productBox.querySelector('.productSubTotal')
        let id = $(this).attr('data-id')
        console.log(id)
        fetch(`http://127.0.0.1:8000/cart/plus-quantity/?cart_id=${id}`,).then(data=>{
            return data.json()
        }).then(res => {
            console.log(res)
            if (res.status == 200){
                qtyElem.value = res.quantity
                productSub.innerHTML = res.price
                priceSetup()
            }
            else {
                alert(`Only ${res.quantity} this quantites of this product is left can't increase anymore :(`)
            }
        })
    })
    $('.qty-minus').click(function(){
        let qtyElem = this.parentElement.parentElement.children[1]
        let productBox = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement
        let productSub = productBox.querySelector('.productSubTotal')
        let id = $(this).attr('data-id')
        console.log(id)
        fetch(`http://127.0.0.1:8000/cart/minus-quantity/?cart_id=${id}`,).then(data=>{
            return data.json()
        }).then(res => {
            console.log(res)
            if (res.status === 200){
                qtyElem.value = res.quantity
                productSub.innerHTML = res.price
                priceSetup()
            }
            else {
                // console.log(this.closest(".product-box-contain"));
                $(this).closest(".product-box-contain").fadeOut("slow", function () {
                    $(this).fadeOut('slow', function(){
                        fetch(`http://127.0.0.1:8000/cart/remove-cart/?cart_id=${id}`).then(data => {
                            return data.json()
                        }).then(res => {
                            console.log(res);
                            priceSetup()
                        })
                    })
                })
            }
        })
    })
}

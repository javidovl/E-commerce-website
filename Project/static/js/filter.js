current_pathname = window.location.pathname


const filter = {

    _items: [],

    getData: (query) => {
        const url = new URL(`http://localhost:8000` + '/api/product_version/' + `?` + query);
        fetch(url).then(response => response.json())
            .then(data => filter.setItems(data));

    },

    setItems: (data) => {
        filter._items = data
    },

    getItems: () => {
        return filter._items
    },
}


document.querySelectorAll('.parent_category, .subcats').forEach(item => {
    item.addEventListener('click', event => {
        filter.getData(`category=${item.getAttribute("category_id")}`)
        setTimeout(aldas, 500)
    })
})


function aldas() {
    document.querySelector("#list").children[0].innerHTML = ""
    for (let i = 0; i < filter.getItems().length; i++) {
        item = filter._items[i]
        $("#list").children(".col-xs-12").append(`<div class="single-list-view">
        <div class="row">
            <div class="col-xs-12 col-md-4">
                <div class="list-img">
                    <div class="product-img">
                        <div class="pro-type sell">
                            <span>sell</span>
                        </div>
                        <a href=""${location.origin}/product/${filter._items[i].product}""><img src="${filter._items[i].image_url}" alt="Product Title" /></a>
                    </div>
                </div>
            </div>
            <div class="col-xs-12 col-md-8">
                <div class="list-text">
                    <h3>${item.name}</h3>
                    <span>${item.category_name}</span>
                    <div class="ratting floatright">
                    <p>( ${item.review_count} Reviews )</p>
                    </div>
                    <h5>$${item.price}</h5>
                    <p>${item.description.substring(0, 120)}</p>
                    
                </div>
            </div>
        </div>
    </div>`)
    }
}


document.querySelectorAll('.parent_category').forEach(item => {
    $(item).parent('.panel').hover(
        function () {
            $(this).children('.collapse').collapse('show');
        }, function () {
            $(this).children('.collapse').collapse('hide');
        }
    );
})

document.querySelectorAll('.oneofsize').forEach(item => {
    $(item).click(
        function () {
            filter.getData(`size=${item.getAttribute("size")}`), setTimeout(aldas, 100)
        }
    )
})

$('.colors_for_filter').children("span").each(function () {
    $(this).click(
        function () {
            filter.getData(`color=${this.getAttribute("color")}`), setTimeout(aldas, 100)
        }
    )
})





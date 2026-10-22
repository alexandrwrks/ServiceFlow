async function getTestDAta() {
    const orders = [
        {
            id: 1,
            title: "Test Data 1",
            description: "Test Description 1",
            status: "success",
            price: 5000
        },
        {
            id: 2,
            title: "Test Data 2",
            description: "Test Description 2",
            status: "warning",
            price: 5000
        },
        {
            id: 3,
            title: "Test Data 3",
            description: "Test Description 3",
            status: "cancelled",
            price: 5000
        }
    ];

    const container = document.getElementById("orders-container");

    orders.forEach(order => {
        const card = document.createElement('div');

        card.classList.add('order-card');

        card.innerHTML = `
            <h2>${order.title}</h2>
            <p>${order.description}</p>
            <p>Статус: ${order.status}</p>
            <p>Цена: ${order.price}</p>
       `;

        container.appendChild(card);
    });


    console.log("Проверка");
}


getTestDAta();
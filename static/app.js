const $cupcakes = $("#cupcakes");
const $newCupcakeForm = $("#new-cupcake-form");

async function displayCupcakes() {
	let cupcakes = await listCupcakes();

	for (const cupcake of cupcakes) {
		appendCupcake(cupcake);
	}
}

async function listCupcakes() {
	const resp = await axios.get("/api/cupcakes");
	return resp.data.cupcakes;
}

function appendCupcake(cupcake) {
	$card = $("<div>").addClass("card cupcake m-1");
	$image = $("<img>").attr("src", cupcake.image).addClass("card-img-top");
	$body = $(`
    <div class="card-body">
        <h5 class="card-title">${cupcake.flavor}</h5>
        <p class="card-text">
            Rating: <b>${cupcake.rating}</b>
            <br>
            Size: <b>${cupcake.size}</b>
        </p>
    </div>
    `);

	$card.append($image);
	$card.append($body);
	$cupcakes.append($card);
}

function handleSubmit(event) {
	event.preventDefault();

	const flavor = $("#form-flavor").val();
	const rating = $("#form-rating").val();
	const size = $("#form-size").val();
	const image = $("#form-image").val();

	const cupcake = {
		flavor,
		size,
		rating,
	};

	if (image) {
		cupcake.image = image;
	}

	createCupcake(cupcake);
}

async function createCupcake(cupcake) {
	const resp = await axios.post(`/api/cupcakes`, cupcake);
	appendCupcake(resp.data.cupcake);
	$newCupcakeForm.trigger("reset");
}

displayCupcakes();
$newCupcakeForm.submit(handleSubmit);

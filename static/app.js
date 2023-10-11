$(document).ready(function(){

    async function loadCupcakes(){
        const cupcakes = await axios.get('/api/cupcakes')
        console.log(cupcakes)

        for(let cupcake of cupcakes.data.cupcakes){
            addToCupcakeLi(cupcake)
        }
    }

    function addToCupcakeLi(cupcake){
        $('#cupcake-list').append(
            `<li> 
                <img class=".img-thumbnail" src="${cupcake['image']}" alt=""> 
                <b>${cupcake.flavor}</b>, 
                ${cupcake.size} - ${cupcake.rating} rating  
                <button class = "delete-cupcake" data-id=${cupcake.id}>Delete</button> 
            </li>`)
    }

    loadCupcakes()

    $(document).on('click', '.delete-cupcake', deleteCupcake)
            
    async function deleteCupcake(){
        const cupcake = $(this).data('id')
        await axios.delete(`/api/cupcakes/${cupcake}`)
        $(this).parent().remove()
    }


    const form = document.querySelector("#form")
    form.addEventListener("submit", async function(e){
        e.preventDefault()
        const flavorInput = document.querySelector('#flavor')
        const flavorText = flavorInput.value
        const sizeInput = document.querySelector('#size')
        const sizeText = sizeInput.value
        const ratingInput = document.querySelector('#rating')
        const ratingText = ratingInput.value
        const imageInput = document.querySelector('#image')
        let imageText = imageInput.value

            if (imageText.value=""){
                imageText.value = 'https://tinyurl.com/demo-cupcake'
            }
        
        const new_cupcake = await axios.post('/api/cupcakes', 
                                {flavor : flavorText, 
                                    size: sizeText, 
                                    rating: ratingText, 
                                    image:imageText.value})

        addToCupcakeLi(new_cupcake.data.cupcake)

        flavorInput.value = ''
        sizeInput.value = ''
        ratingInput.value = ''
        imageInput.value = ''
    })



})





    





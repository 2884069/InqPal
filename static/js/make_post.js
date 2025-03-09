document.getElementById('picture_input').addEventListener('change', function ImageChanged(){
    if (this.files.length === 0) {
        document.getElementById('picture_preview').src = placeholderImage;
        console.log('No image selected.');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function fileReadCompleted() {
        document.getElementById('picture_preview').src = reader.result;
    };
    reader.readAsDataURL(this.files[0]);
});
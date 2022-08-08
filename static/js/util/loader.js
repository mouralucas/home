function load(status) {
    switch (status) {
        case "off":
            document.getElementsByClassName('main')[0].style.opacity = "1";
            $(document.getElementsByClassName('main')[0]).removeClass('isDisabled');
            document.getElementsByClassName('loaderBase')[0].style.display = "none";
            break;
        case "on":
            document.getElementsByClassName('main')[0].style.opacity = "0.5";
            $(document.getElementsByClassName('main')[0]).addClass('isDisabled');
            document.getElementsByClassName('loaderBase')[0].style.display = "block";
            break;
        default:
            document.getElementsByClassName('main')[0].style.opacity = "1";
            $(document.getElementsByClassName('main')[0]).removeClass('isDisabled');
            document.getElementsByClassName('loaderBase')[0].style.display = "none";
    }
}
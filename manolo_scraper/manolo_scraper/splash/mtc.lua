function setup_casperjs(splash)
    splash:autoload("https://rawgit.com/n1k0/casperjs/master/modules/clientutils.js")
    splash:autoload([[
        window.__utils__ = new ClientUtils({});
    ]])
end

-- TODO: Use functions instead of string concatenation.
function main(splash)

    setup_casperjs(splash)
    splash:go(splash.args.url)
    splash:wait(0.5)

    splash:runjs([[
        var element = __utils__.getElementByXPath("//select[@name='ctl00$ContentPlaceHolder$ddlUnidad']/option[@value='1']")
        element.selected = true;

        var selector = __utils__.getElementByXPath("//select[@name='ctl00$ContentPlaceHolder$ddlUnidad']")
        selector.onchange();
    ]])
    splash:wait(1.0)

    splash:runjs([[
        var element = __utils__.getElementByXPath("//select[@name='ctl00$ContentPlaceHolder$ddlUnidadOrg']/option[@value='1']")
        element.selected = true;

        var selector = __utils__.getElementByXPath("//select[@name='ctl00$ContentPlaceHolder$ddlUnidadOrg']")
        selector.onchange();
    ]])
    splash:wait(0.5)

    splash:runjs([[
        var element = __utils__.getElementByXPath("//input[@id='ctl00_ContentPlaceHolder_txtDesde']");
        element.value = ']] .. splash.args.start_date .. [[';
        var element = __utils__.getElementByXPath("//input[@id='ctl00_ContentPlaceHolder_txtHasta']")
        element.value = ']] .. splash.args.end_date .. [[';
    ]])

    splash:wait(0.5)

    splash:runjs([[
        var button = __utils__.getElementByXPath("//button[@id='ctl00_ContentPlaceHolder_btnConsultar']")
        button.click()
    ]])

    splash:wait(10.0)

    return {
        html = splash:html(),
    }
end
from django.shortcuts import render


def index(request):
    return render(request, "hello/index.html")


def available_inventory(request):
    return render(
        request,
        "hello/page_stub.html",
        {
            "page_title": "Available Inventory",
            "page_heading": "Available Inventory",
            "page_description": (
                "This page will list currently available donations with search, "
                "filtering, and pagination in a later checkpoint."
            ),
        },
    )


def requested_items(request):
    return render(
        request,
        "hello/page_stub.html",
        {
            "page_title": "Requested Items",
            "page_heading": "Requested Items",
            "page_description": (
                "This page will highlight the items the organization currently "
                "needs so donors can respond."
            ),
        },
    )


def distributed_items(request):
    return render(
        request,
        "hello/page_stub.html",
        {
            "page_title": "Distributed Items",
            "page_heading": "Distributed Items",
            "page_description": (
                "This page will hold distribution history and assignment records "
                "once the inventory workflow is implemented."
            ),
        },
    )

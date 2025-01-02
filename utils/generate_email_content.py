def generate_email_html_content(customer_info: dict, order_info: dict):

    order_number = order_info["order_number"]
    ordered_items = order_info["ordered_items"]
    total_cost = order_info["total_cost"]
    preselection_items = ordered_items.get("preselection_items", None)
    custom_items = ordered_items.get("custom_items", None)

    html_content = f"""
    <html>
        <body>
            <p style="font-size: 32px; margin-bottom: 16px;">Thank you for your order!</p>
            <p>Now you can relax. We're working on getting your gifts to you ASAP!</p>
            <hr />
            <p style="font-size: 20px; margin-bottom: 16px;">Order Summary</p>
            <p>Order number: {order_number}</p>
    """

    if preselection_items:
        html_content += f"""
        <div>
            <p style="font-weight: 700;">Preselection gifts:</p>
        """

        for index, preselection in enumerate(preselection_items):
            html_content += f"""
                <div>
                    <div style="display: flex; flex-direction: row; justify-content: space-between;">
                        <p>#{(index + 1)} x {preselection["quantity"]}</p>
                        <p>Item subtotal: ${preselection["price_with_quantity"]}
                    </div>
                    <p>Preselection: {preselection["name"]}
                </div>
            """
        
        html_content += f"""
        </div>
        """

    if custom_items:
        html_content += f"""
        <div>
            <p style="font-weight: 700;">Custom gifts:</p>
        """

        for index, custom_item in enumerate(custom_items):
            html_content += f"""
                <div>
                    <div style="display: flex; flex-direction: row; justify-content: space-between;">
                        <p>#{(index + 1)} x {custom_item["quantity"]}</p>
                        <p>Item subtotal: ${custom_item["price_with_quantity"]}
                    </div>
                    <p>Bag: {custom_item["bag_name"]}
                """
            
            for index, item in enumerate(custom_item["item_names"]):
                html_content += f"""
                    <p>Item {(index + 1)}: {item}
                """
            
            html_content += f"""
                </div>
            """

        html_content += f"""
            <div style="display: flex; flex-direction: row; justify-content: space-between;">
                <p>Order total (GST Inc.)</p>
                <p>${total_cost}</p>
            </div>
        </div>
        """

    html_content += f"""
        <hr />
        <p style="font-size: 20px; margin-bottom: 16px;">Your Details</p>
        <p>{customer_info["first_name"]} {customer_info["last_name"]}</p>
        <p>{customer_info["mobile"]}</p>
        <p>{customer_info["email"]}</p>
    """

    html_content += """
        </body>
    </html>
    """

    return html_content

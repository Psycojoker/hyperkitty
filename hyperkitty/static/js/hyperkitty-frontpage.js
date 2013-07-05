/*
 * Copyright (C) 1998-2012 by the Free Software Foundation, Inc.
 *
 * This file is part of HyperKitty.
 *
 * HyperKitty is free software: you can redistribute it and/or modify it under
 * the terms of the GNU General Public License as published by the Free
 * Software Foundation, either version 3 of the License, or (at your option)
 * any later version.
 *
 * HyperKitty is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
 * more details.
 *
 * You should have received a copy of the GNU General Public License along with
 * HyperKitty.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Author: Aurelien Bompard <abompard@fedoraproject.org>
 */


/*
 * List descriptions on the front page
 */
function update_list_properties(url) {
    $.ajax({
        dataType: "json",
        url: url,
        success: function(data) {
            $(".all-lists .mailinglist").each(function() {
                var name = $(this).find(".list-address").text();
                if (!data[name]) {
                    return;
                }
                if (data[name]["display_name"]) {
                    $(this).find(".list-name").text(data[name]["display_name"]);
                }
                if (data[name]["description"]) {
                    $(this).find(".list-description")
                           .text(data[name]["description"]);
                }
            });
        },
        error: function(jqXHR, textStatus, errorThrown) {
            //alert(jqXHR.responseText);
        },
        complete: function(jqXHR, textStatus) {
            $(".all-lists .mailinglist img.ajaxloader").remove();
        }
    });
}
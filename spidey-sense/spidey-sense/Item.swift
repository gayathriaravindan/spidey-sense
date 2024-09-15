//
//  Item.swift
//  spidey-sense
//
//  Created by Gayathri Aravindan on 9/14/24.
//

import Foundation
import SwiftData

@Model
final class Item {
    var timestamp: Date
    
    init(timestamp: Date) {
        self.timestamp = timestamp
    }
}

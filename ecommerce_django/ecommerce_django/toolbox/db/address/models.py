from django.db import models


class AbstractAddressModel(models.Model):

    block_number = models.CharField(max_length=10, blank=True, null=True)
    street_name = models.CharField(max_length=255, blank=True, null=True)
    level_number = models.CharField(max_length=5, blank=True, null=True)
    unit_number = models.CharField(max_length=30, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    building_name = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_full_address()

    def get_full_address(self):
        address = []

        if self.block_number:
            address.append("Block {0}".format(self.block_number))

        if self.street_name:
            address.append(self.street_name.title())

        if self.level_number and self.unit_number:
            address.append("#{0}-{1}".format(self.level_number, self.unit_number))
        elif self.level_number and not self.unit_number:
            address.append("#{0}".format(self.level_number))
        elif not self.level_number and self.unit_number:
            address.append("#??-{0}".format(self.unit_number))

        if self.building_name:
            address.append(self.building_name)

        if self.landmark:
            address.append(self.landmark)

        if self.postal_code:
            address.append("Singapore {0}".format(self.postal_code))

        return ", ".join(address)

    def get_short_address(self):
        address = []

        if self.block_number:
            address.append("Block {0}".format(self.block_number))

        if self.street_name:
            address.append(self.street_name.title())

        if self.level_number and self.unit_number:
            address.append("#{0}-{1}".format(self.level_number, self.unit_number))
        elif self.level_number and not self.unit_number:
            address.append("#{0}".format(self.level_number))
        elif not self.level_number and self.unit_number:
            address.append("#??-{0}".format(self.unit_number))

        if self.building_name:
            address.append(self.building_name)

        return ", ".join(address)

    def get_address_line1(self):
        address = []

        if self.block_number:
            address.append("Block {0}".format(self.block_number))

        if self.street_name:
            address.append(self.street_name.title())

        return ", ".join(address)

    def get_address_line2(self):
        address = []

        if self.level_number and self.unit_number:
            address.append("#{0}-{1}".format(self.level_number, self.unit_number))
        elif self.level_number and not self.unit_number:
            address.append("#{0}".format(self.level_number))
        elif not self.level_number and self.unit_number:
            address.append("#??-{0}".format(self.unit_number))

        if self.building_name:
            address.append(self.building_name)

        return ", ".join(address)

    def get_postal_code_display(self):
        if self.postal_code:
            return "Singapore {0}".format(self.postal_code)
        return ""

    def get_geo_location(self):
        if self.latitude and self.longitude:
            return (self.latitude, self.longitude)
        return (0.0, 0.0)



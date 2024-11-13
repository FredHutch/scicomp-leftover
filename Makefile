release=${RELEASE}
all:
	echo "No \"all\" target actions set ATM"



debdirs:
	mkdir -p debian/scicomp-leftover_$(release) \
		debian/scicomp-leftover_$(release)/usr \
		debian/scicomp-leftover_$(release)/usr/local \
		debian/scicomp-leftover_$(release)/usr/local/lib \
		debian/scicomp-leftover_$(release)/usr/local/bin \
		debian/scicomp-leftover_$(release)/DEBIAN
	cp debian/control debian/scicomp-leftover_$(release)/DEBIAN/control

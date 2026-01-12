import panel as pn
pn.extension()

import xarray as xr
import hvplot.xarray

sst_anom = xr.open_dataset("data/sst_anomaly_2011_2022.nc")["sst"]
ufi_2025 = xr.open_dataset("data/ufi_2025_monthly.nc")


sst_cold = sst_anom.where(sst_anom < 0)

monsoon_seasons = {
    "NE Monsoon (Dec–Feb)": [12, 1, 2],
    "Inter-monsoon (Mar–May)": [3, 4, 5],
    "SW Monsoon (Jun–Sep)": [6, 7, 8, 9],
    "Inter-monsoon (Oct–Nov)": [10, 11],
}

phases = {
    "Onset (June)": [6],
    "Peak (July–August)": [7, 8],
    "Relaxation (September)": [9],
}

season_select = pn.widgets.RadioButtonGroup(
    name="Season",
    options=list(monsoon_seasons.keys()),
    button_type="primary"
)


wind_toggle = pn.widgets.Checkbox(
    name="Show 2025 Wind Forcing",
    value=True
)

def upwelling_map(season, show_wind):
    months = monsoon_seasons[season]

    sst_map = (
        sst_cold
        .sel(time=sst_cold.time.dt.month.isin(months))
        .mean("time")
        .hvplot.quadmesh(
            cmap="Blues_r",
            clim=(-2, 0),
            geo=True,
            coastline=True,
            frame_width=700,
            frame_height=500,
            title=f"{season}: Upwelling-Driven Cooling (2011–2022)",
            colorbar=True
        )
    )

    if show_wind:
        ufi_map = (
            ufi_2025
            .isel(time=[5,6,7,8])
            .mean("time")
            .hvplot.contour(
                geo=True,
                levels=8,
                line_color="black"
            )
        )
        return sst_map * ufi_map

    return sst_map

dashboard = pn.Column(
    "# Horn of Africa Upwelling Dashboard",
    "### Seasonal upwelling patterns based on SST anomalies and wind forcing",
    pn.Row(season_select, wind_toggle),
    pn.bind(upwelling_map, season_select, wind_toggle)
)

dashboard.servable()


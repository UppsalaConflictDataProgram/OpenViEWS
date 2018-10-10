echo "Running all plot scripts in sequence"

bash plot_desc_cm.sh &
bash plot_desc_pgm.sh &
bash plot_featimp.sh &
wait
bash plot_maps_cm.sh &
bash plot_maps_pgm.sh &
bash plot_maps_features.sh &
wait
echo "Finished all plotting scripts"
